from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from datetime import datetime
from sqlalchemy import Integer, func, ForeignKey

from database.config import settings

DATABASE_URL = settings.get_sqlite_db_url()

# Create async engine for DB work
engine = create_async_engine(url=DATABASE_URL)
# Create session fabric for DB interaction
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Models Base Class
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Abstract class (No table created for it)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
