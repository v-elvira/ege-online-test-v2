from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_items(self) -> list[Item]:
        result = await self.db.scalars(select(Item).order_by(Item.id))
        return list(result.all())

    async def get_item(self, item_id: int) -> Item | None:
        return await self.db.get(Item, item_id)

    async def create_item(self, payload: ItemCreate) -> Item:
        item = Item(title=payload.title, description=payload.description)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_item(self, item: Item, payload: ItemUpdate) -> Item:
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(item, field, value)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_item(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.commit()
