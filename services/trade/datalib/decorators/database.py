from typing import Callable, Awaitable, Any, Type, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy import func as sqlalchemy_func, or_
from pydantic import BaseModel
from functools import wraps


def paginated(
    schema: Type[BaseModel],
    search_fields: Sequence[Any] = (),
    scalars: bool = True,
):
    """
    Decorator that paginates and optionally searches the result of a SQLAlchemy select statement.

    :param schema: Pydantic schema to serialize results
    :param search_fields: list of SQLAlchemy columns to search with LIKE
    """

    def decorator(query_fn: Callable[..., Awaitable[Select]]):
        @wraps(query_fn)
        async def wrapper(
            *args,
            db: AsyncSession,
            limit: int = 10,
            offset: int = 0,
            search: str = None,
            **kwargs,
        ) -> dict[str, Any]:
            stmt: Select = await query_fn(*args, db=db, **kwargs)

            # Apply search if applicable
            if search and search_fields:
                search_term = f"%{search.lower()}%"
                stmt = stmt.where(
                    or_(
                        sqlalchemy_func.lower(field).like(search_term)
                        for field in search_fields
                    )
                )

            # Total count for pagination metadata
            count_stmt = stmt.with_only_columns(sqlalchemy_func.count()).order_by(None)
            total = await db.scalar(count_stmt)

            # Apply offset/limit
            paginated_stmt = stmt.offset(offset).limit(limit)
            result = await db.execute(paginated_stmt)

            # Try scalar response (single-model); fallback to mappings (joined/aliased)
            if scalars:
                records = result.scalars().all()
                data = [schema.model_validate(r) for r in records]
            else:
                records = result.mappings().all()
                data = [schema(**r) for r in records]

            return {
                "data": data,
                "total": total,
            }

        return wrapper

    return decorator
