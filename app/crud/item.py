import uuid
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemPartialUpdate


async def count_items(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Item))
    return result.scalar_one()


async def get_items(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10,
) -> List[Item]:
    """
    Retrieve all items with pagination.

    Args:
        db (AsyncSession): Database session.
        page (int): Number of records to page.
        page_size (int): Maximum number of records to return.

    Returns:
        List[Item]: List of item ORM objects.
    """
    query = select(Item).offset(page - 1).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all()


async def get_item(
    db: AsyncSession,
    item_id: uuid.UUID,
) -> Optional[Item]:
    """
    Retrieve a single item by ID.

    Args:
        db (AsyncSession): Database session.
        item_id (UUID): Item identifier.

    Returns:
        Optional[Item]: Item if found, otherwise None.
    """
    query = select(Item).filter(Item.id == item_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_item(
    db: AsyncSession,
    item: ItemCreate,
) -> Item:
    """
    Create a new item record.

    Args:
        db (AsyncSession): Database session.
        item (ItemCreate): Input payload.

    Returns:
        Item: Created item instance.
    """
    db_item = Item(**item.model_dump())
    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item


async def update_item(
    db: AsyncSession,
    db_item: Item,
    item_update: ItemPartialUpdate,
) -> Item:
    """
    Update an existing item record.

    Args:
        db (AsyncSession): Database session.
        db_item (Item): Existing ORM item.
        item_update (ItemUpdate): Fields to update.

    Returns:
        Item: Updated item.
    """
    update_data = item_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return db_item


async def delete_item(
    db: AsyncSession,
    db_item: Item,
) -> None:
    """
    Delete an item from the database.

    Args:
        db (AsyncSession): Database session.
        db_item (Item): ORM instance to delete.

    Returns:
        None
    """
    await db.delete(db_item)
    await db.commit()
