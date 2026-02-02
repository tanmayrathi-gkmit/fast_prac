from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True only for debugging SQL
    future=True,  # Use SQLAlchemy 2.0 style
    pool_pre_ping=True,  # Detect & refresh broken connections
    pool_recycle=1800,  # Recycle connections every 30 minutes
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    Provides an asynchronous SQLAlchemy session for FastAPI routes.

    Usage:
        db: AsyncSession = Depends(get_db)

    Ensures:
        - The session is created per request
        - Automatically closed after request completes
        - Safe for concurrency

    Yields:
        AsyncSession: A live database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
