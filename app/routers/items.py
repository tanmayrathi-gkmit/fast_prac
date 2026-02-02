from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import item as item_crud
from app.database.session import get_db
from app.schemas.item import (
    ItemCreate,
    ItemListResponse,
    ItemPartialUpdate,
    ItemResponse,
)

router = APIRouter()


@router.get("/", response_model=ItemListResponse, status_code=status.HTTP_200_OK)
async def read_items(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve items with pagination metadata.

    Args:
        page (int): Number of items to page for pagination.
        page_size (int): Maximum number of items to return.
        db (AsyncSession): SQLAlchemy async session.

    Returns:
        ItemListResponse: Paginated results containing:
            - total: Total items in DB
            - count: Number of items returned
            - page: Pagination offset
            - page_size: Pagination page_size
            - data: List[ItemResponse]
    """
    items = await item_crud.get_items(db, page=page, page_size=page_size)

    # Count total rows in DB
    total = await item_crud.count_items(db)

    return ItemListResponse(
        total=total,
        count=len(items),
        page=page,
        page_size=page_size,
        data=items,
    )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new item.

    Args:
        item (ItemCreate): Input payload for the new item.
        db (AsyncSession): SQLAlchemy async session.

    Returns:
        ItemResponse: The created item.
    """
    return await item_crud.create_item(db=db, item=item)


@router.get("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def read_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a single item by its ID.

    Args:
        item_id (UUID): Unique identifier of the item.
        db (AsyncSession): Database session.

    Raises:
        HTTPException: If item is not found.

    Returns:
        ItemResponse: Retrieved item.
    """
    item = await item_crud.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.put("/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update_item(
    item_id: UUID,
    item_update: ItemPartialUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing item.

    Args:
        item_id (UUID): ID of the item to update.
        item_update (ItemUpdate): Fields to update.
        db (AsyncSession): SQLAlchemy session.

    Raises:
        HTTPException: If item does not exist.

    Returns:
        ItemResponse: Updated item.
    """
    db_item = await item_crud.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return await item_crud.update_item(db=db, db_item=db_item, item_update=item_update)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an item by ID.

    Args:
        item_id (UUID): ID of the item to delete.
        db (AsyncSession): Database session.

    Raises:
        HTTPException: If the item does not exist.

    Returns:
        None: FastAPI sends 204 No Content.
    """
    item = await item_crud.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    await item_crud.delete_item(db=db, db_item=item)
    return None
