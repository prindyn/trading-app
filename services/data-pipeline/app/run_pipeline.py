import asyncio
import importlib
from typing import Optional, List
from app.core.logger import logger
from app.sources.base import BaseSource
from app.pipelines.base import BasePipeline, PipelineManager
from app.core.registry import PIPELINE_REGISTRATION_MAP


def get_pipeline_map(
    source_filter: Optional[str] = None, pipeline_filter: Optional[str] = None
):
    for pipeline_map in PIPELINE_REGISTRATION_MAP:
        source = pipeline_map.get("source")
        if source_filter and source.__name__.lower() != source_filter.lower():
            continue
        pipelines = pipeline_map.get("pipelines", [])
        if pipeline_filter:
            pipelines = [
                p for p in pipelines if p.__name__.lower() == pipeline_filter.lower()
            ]
        yield pipeline_map, source, pipelines


def load_runner(pipeline_map: dict):
    runner_path = pipeline_map.get("runner")
    if not runner_path:
        return None

    try:
        module = importlib.import_module(runner_path)
        RunnerClass = getattr(module, "PipelineRunner")
        return RunnerClass(pipeline_map)
    except Exception as e:
        logger.error(f"Failed to load runner from '{runner_path}': {e}")
        return None


async def register_all(
    source_filter: Optional[str] = None, pipeline_filter: Optional[str] = None
):
    """
    Create and register all pipelines (or filtered ones).
    Returns list of PipelineManager instances ready to run.
    """
    managers = []
    for pipeline_map, source_cls, pipelines in get_pipeline_map(
        source_filter, pipeline_filter
    ):
        try:
            if not issubclass(source_cls, BaseSource):
                raise TypeError("'source' must be a subclass of BaseSource.")

            runner = load_runner(pipeline_map)
            manager = PipelineManager(source_cls, runner=runner)

            for pipeline in pipelines:
                if not issubclass(pipeline, BasePipeline):
                    raise TypeError("'pipeline' must be a subclass of BasePipeline.")
                await manager.register(pipeline)
                logger.info(
                    f"Registered pipeline '{pipeline.__name__}' for source '{manager.source.name}'"
                )
            managers.append(manager)
        except Exception as error:
            logger.error(
                f"Failed to register pipeline(s) for source '{source_cls}': {str(error)}"
            )
    return managers


async def execute_all(managers: List[PipelineManager]):
    """
    Run all pipelines for the given list of PipelineManagers.
    """
    await asyncio.gather(*(manager.run_all() for manager in managers))


async def run_all(source: Optional[str] = None, pipeline: Optional[str] = None):
    logger.info("Starting pipeline execution for all sources...")
    managers = await register_all(source, pipeline)
    await execute_all(managers)
    logger.info("Completed pipeline execution for all sources.")
