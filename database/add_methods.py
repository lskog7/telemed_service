from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import run

from database.db import connection
from database.models import User


@connection
async def create_user_example_1(username: str, email: str, password: str, session: AsyncSession) -> int:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
    - username: str - имя пользователя
    - email: str - адрес электронной почты
    - password: str - пароль пользователя
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - int - идентификатор созданного пользователя
    """
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id
