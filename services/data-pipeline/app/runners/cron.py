import asyncio
import aiocron
from typing import List
from app.runners.base import BasePipelineRunner
from app.pipelines.base import BasePipeline
from app.core.logger import logger


class PipelineRunner(BasePipelineRunner):
    def __init__(self, pipeline_map):
        self.pipeline_map = pipeline_map

    async def run(self, pipelines: List[BasePipeline]) -> None:
        logger.info("[aiocronRunner] Scheduling pipeline with aiocron...")

        @aiocron.crontab(self.pipeline_map.get("interval"))
        async def job():
            try:
                logger.info("[aiocronRunner] Running pipelines...")
                await asyncio.gather(*(pipeline.run() for pipeline in pipelines))
            except Exception as e:
                logger.error(f"[aiocronRunner] Error in running pipelines: {e}")

        try:
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            logger.info("[aiocronRunner] Exiting aiocron scheduler...")
