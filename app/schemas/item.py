from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Base Shared Fields
# ---------------------------------------------------------------------------
class ItemBase(BaseModel):
    """
    Shared fields across create, update, and response schemas.
    Represents the core editable fields of an item.
    """

    title: str = Field(..., min_length=1, max_length=255, example="Buy groceries")
    description: Optional[str] = Field(
        None,
        example="Milk, Bread, Cheese",
    )
    is_completed: bool = Field(
        False,
        example=False,
        description="Has the item been completed?",
    )


# ---------------------------------------------------------------------------
# Create Schema (Client → API)
# ---------------------------------------------------------------------------
class ItemCreate(ItemBase):
    """
    Fields required when creating a new item.
    Inherits all fields from ItemBase.
    """

    pass


# ---------------------------------------------------------------------------
# Update Schema (Partial Update)
# ---------------------------------------------------------------------------
class ItemPartialUpdate(BaseModel):
    """
    Patch-like update schema for Item.
    Only updates provided fields.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = None

    model_config = {"extra": "ignore"}


# ---------------------------------------------------------------------------
# Response Schema (API → Client)
# ---------------------------------------------------------------------------
class ItemResponse(ItemBase):
    """
    Schema returned to the client after read/create/update.
    Includes server-managed fields like ID and timestamps.
    """

    id: UUID = Field(..., example="d240b6a5-2f8a-4f93-9f33-91b3f7c8b410")
    created_at: datetime = Field(..., example="2024-01-01T12:00:00Z")
    updated_at: Optional[datetime] = Field(None, example="2024-01-02T15:00:00Z")

    model_config = {
        "from_attributes": True  # Pydantic v2 equivalent of orm_mode=True
    }


class ItemListResponse(BaseModel):
    """
    Wrapper response for paginated items list.
    """

    total: int  # Total items in DB
    count: int  # Count of items in this page
    page: int  # Current offset
    page_size: int  # Page size
    data: List[ItemResponse]
