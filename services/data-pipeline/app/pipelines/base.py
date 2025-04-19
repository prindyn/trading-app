import functools
import asyncio
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator
from datetime import datetime
from app.sources.base import BaseSource
from app.storage.base import BaseStorage
from app.clients.base import BaseClient
from app.storage.local import LocalStorage
from app.runners.base import BasePipelineRunner
from app.core.logger import logger


def pipeline_duration(func):
    @functools.wraps(func)
    async def wrapper(self: "BasePipeline", *args, **kwargs):
        logger.info(f"Running pipeline: {self.name}")
        start_time = datetime.utcnow()
        result = await func(self, *args, **kwargs)
        duration = datetime.utcnow() - start_time
        logger.info(f"Finished running pipeline: {self.name} in {duration}")
        return result

    return wrapper


class BasePipeline(ABC):
    name: str = "base"

    def __init__(
        self,
        source: BaseSource,
        name: str = "",
        config: dict = {},
        storage: BaseStorage = None,
    ):
        self.source = source
        self.config = config
        self.storage = storage or LocalStorage()
        self.name = f"{self._name}_{name}" if name else self._name

    @pipeline_duration
    async def run(self):
        """
        Full pipeline execution: fetch, validate, save.
        """
        if not self.should_run():
            logger.info(f"Skipping pipeline: {self.name} (not scheduled)")
            return

        data = await self.fetch_data()
        self.validate_data(data)
        metadata = self.build_metadata()
        await self.populate(data, metadata)

    async def populate(self, data, metadata):
        """
        Aggregate and save data to storage.
        """
        logger.info(f"Populating data for pipeline: {self.name}")
        await self.storage.aggregate_and_save(data, metadata)

    def build_metadata(self) -> Dict[str, Any]:
        """
        Build metadata for the pipeline run.
        """
        return {
            "pipeline": self.name,
            "timestamp": datetime.utcnow().isoformat(),
            **self.config,
        }

    def should_run(self) -> bool:
        """
        Check if the pipeline should run based on the configured interval.
        """
        return True

    @property
    def _name(self):
        """
        Returns the name of the pipeline based on class name.
        """
        return self.__class__.__name__.replace("Pipeline", "").lower()

    @abstractmethod
    async def fetch_data(self):
        """
        Fetch data from the configured source.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_data(self, data):
        """
        Validate the fetched data.
        """
        raise NotImplementedError


class PipelineManager:
    def __init__(self, source: BaseSource, runner: BasePipelineRunner = None):
        """
        Manager class to register and run multiple pipelines.
        :param source: The source instance that uses this pipeline manager.
        """
        self.source: BaseSource = source()
        self.runner: BasePipelineRunner = runner
        self.pipelines: List[BasePipeline] = []

    async def register(self, pipeline: BasePipeline) -> None:
        """
        Register a new pipeline.
        :param pipeline: The pipeline class to register.
        """
        async for p in self._gen_pipelines(pipeline):
            self.pipelines.append(p)

    async def _gen_pipelines(self, pipeline) -> AsyncGenerator:
        """
        Generate pipelines based on the source's active pairs and intervals.
        :param pipeline: The pipeline class to generate.
        """
        active_pairs = await self.source.get_active_pairs()
        intervals = await self.source.get_intervals()
        client_cls = self.source.get_client_cls(pipeline)

        if not client_cls:
            logger.error(
                f"Failed to get client class for pipeline '{pipeline.__name__}'"
            )
            return

        client: BaseClient = client_cls(self.source.base_url)
        seen_keys = set()

        for pair in active_pairs:
            for interval in intervals:
                payload = {"symbol": pair, "interval": interval}

                try:
                    params = client.build_params(payload)
                except Exception as e:
                    logger.warning(
                        f"Invalid config for pair={pair}, interval={interval}: {e}"
                    )
                    continue

                key = json.dumps(params, sort_keys=True)
                # Skip duplicate pipelines
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                # Generate pipeline name
                safe_name_parts = [
                    str(v) for v in params.values() if isinstance(v, (str, int))
                ]
                pipeline_name = (
                    f"{self.source.name}_{'_'.join(safe_name_parts)}"
                    if safe_name_parts
                    else self.source.name
                )

                logger.info(
                    f"Generating pipeline {pipeline.__name__} for {pipeline_name}"
                )
                yield pipeline(
                    source=self.source,
                    name=pipeline_name,
                    config=payload,
                )

    async def run_all(self):
        """
        Run all registered pipelines in parallel.
        """
        if self.runner:
            await self.runner.run(self.pipelines)
        else:
            await asyncio.gather(*(self._safe_run(p) for p in self.pipelines))

    async def _safe_run(self, pipeline: BasePipeline):
        """
        Run a pipeline with error handling.
        """
        try:
            await pipeline.run()
        except Exception as error:
            logger.error(f"Failed to run pipeline '{pipeline.name}': {str(error)}")
