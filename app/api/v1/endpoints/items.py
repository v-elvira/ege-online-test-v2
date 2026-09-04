from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_item_service
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("/", response_model=list[ItemRead])
async def list_items(service: ItemService = Depends(get_item_service)) -> list[ItemRead]:
    return await service.list_items()


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, service: ItemService = Depends(get_item_service)) -> ItemRead:
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
) -> ItemRead:
    return await service.create_item(payload)


@router.patch("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
) -> ItemRead:
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return await service.update_item(item, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, service: ItemService = Depends(get_item_service)) -> None:
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await service.delete_item(item)
