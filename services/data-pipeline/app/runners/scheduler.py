import uuid
import asyncio
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.runners.base import BasePipelineRunner
from app.pipelines.base import BasePipeline
from app.core.logger import logger


class PipelineRunner(BasePipelineRunner):
    def __init__(self, pipeline_map):
        self.pipeline_map = pipeline_map
        self.scheduler = AsyncIOScheduler()
        self.trigger = self._build_trigger()
        self.pipelines: List[BasePipeline] = []
        self.loop = asyncio.get_event_loop()  # capture main loop during init

    async def run(self, pipelines: List[BasePipeline]) -> None:
        logger.info("[APSchedulerRunner] Scheduling all pipelines as one job...")
        self.pipelines = pipelines

        self.scheduler.add_job(
            id=str(uuid.uuid4()),
            func=lambda: asyncio.run_coroutine_threadsafe(self._start(), self.loop),
            trigger=self.trigger,
            replace_existing=True,
        )

        self.scheduler.start()

        try:
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            logger.info("[APSchedulerRunner] Shutting down scheduler...")
            self.scheduler.shutdown()

    def _build_trigger(self) -> CronTrigger:
        return CronTrigger.from_crontab(self.pipeline_map.get("interval"))

    async def _start(self) -> None:
        logger.info("[APSchedulerRunner] Running scheduled pipeline group...")
        await asyncio.gather(*(p.run() for p in self.pipelines))
