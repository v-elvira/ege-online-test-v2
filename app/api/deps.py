from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.item import ItemService


async def get_item_service(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ItemService, None]:
    yield ItemService(db)
