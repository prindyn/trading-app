import asyncio
from app.core.logger import logger
from app.run_pipeline import register_all, execute_all


async def main():
    logger.info("Registering pipelines on app startup...")
    managers = await register_all()

    logger.info("Starting all registered pipeline runners...")
    await execute_all(managers)


if __name__ == "__main__":
    asyncio.run(main())
