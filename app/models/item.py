import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class Item(Base):
    """
    Represents a single task/item in the system.

    Fields:
        id (UUID): Primary key with PostgreSQL native UUID type.
        title (str): Short title of the item.
        description (str | None): Optional detailed description.
        is_completed (bool): Marks completion state.
        created_at (datetime): Auto-set on creation.
        updated_at (datetime | None): Auto-updated on modification.
    """

    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key — UUID v4",
    )

    title: Mapped[str] = mapped_column(
        String(length=255),
        index=True,
        nullable=False,
        comment="Short title for item",
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        comment="Optional description field",
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Status: completed or not",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when item was created",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="Timestamp when item was last updated",
    )
