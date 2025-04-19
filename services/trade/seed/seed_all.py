import json
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_session_async
from app.models import tables

DATA_DIR = Path(__file__).parent / "data"

# Explicit seeding order based on dependencies
SEED_ORDER = [
    "asset",
    "exchange",
    "trade_pair",
]

# Optional unique key overrides
UNIQUE_KEYS = {"asset": "symbol", "exchange": "name"}


def get_model_class(model_name: str):
    class_name = "".join(part.capitalize() for part in model_name.split("_"))
    return getattr(tables, class_name, None)


def filter_model_fields(model, record: dict) -> dict:
    model_columns = model.__table__.columns.keys()
    return {key: value for key, value in record.items() if key in model_columns}


async def seed_file(session: AsyncSession, model_name: str, file_path: Path):
    model = get_model_class(model_name)
    if model is None:
        print(f"Model '{model_name}' not found. Skipping {file_path.name}")
        return

    unique_key = UNIQUE_KEYS.get(model_name, "id")

    with open(file_path, "r") as f:
        records = json.load(f)

    added = 0
    for record in records:
        if unique_key not in record:
            print(f"Skipping record without '{unique_key}' in {file_path.name}")
            continue

        stmt = select(model).where(getattr(model, unique_key) == record[unique_key])
        result = await session.execute(stmt)
        if result.scalar():
            continue

        session.add(model(**filter_model_fields(model, record)))
        added += 1

    await session.commit()
    print(f"{file_path.name}: {added} new records seeded")


async def main():
    async with get_session_async() as session:
        for model_name in SEED_ORDER:
            file_path = DATA_DIR / f"{model_name}.json"
            if file_path.exists():
                await seed_file(session, model_name, file_path)
            else:
                print(f"Skipping {model_name}.json — file not found")


if __name__ == "__main__":
    asyncio.run(main())
