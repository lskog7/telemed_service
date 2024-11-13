from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from asyncio import run
from typing import Dict, List

from database.db import connection
from database.models import Role, User, Patient, Profile, Hospital
from database.sql_enums import RoleEnum, ProfessionEnum, GenderEnum  # Убедитесь, что вы импортируете RoleEnum


# Get Role ID by it's name
@connection
async def get_role_id(role_name: str, session: AsyncSession) -> Dict[str, int]:
    result = await session.execute(select(Role).where(Role.name == role_name.lower()))
    role = result.scalars().first()

    if role is None:
        raise ValueError(f"Роль {role} не найдена в базе данных.")

    return {"role_id": role.id}


# Fill Roles table with it's default values
@connection
async def add_roles(session: AsyncSession) -> None:
    """
    Добавляет роли в таблицу Roles на основе RoleEnum.

    Аргументы:
        session: AsyncSession - асинхронная сессия базы данных
    """
    for role in RoleEnum:
        # Проверяем, существует ли роль в базе данных
        result = await session.execute(select(Role).where(Role.name == role.value))
        existing_role = result.scalars().first()

        if existing_role is None:
            # Если роль не существует, создаем новую
            new_role = Role(name=role.value)
            session.add(new_role)

    await session.commit()  # Сохраняем изменения в базе данных


@connection
async def create_user(username: str, email: str, password: str, role: str, session: AsyncSession) -> Dict[str, int]:
    """
    Создает нового пользователя с использованием ORM SQLAlchemy.

    Аргументы:
        username: str - имя пользователя
        email: str - адрес электронной почты
        password: str - пароль пользователя
        session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
        int - идентификатор созданного пользователя
    """
    # Получаем роль из базы данных
    result = await session.execute(select(Role).where(Role.name == role))
    role = result.scalars().first()

    if role is None:
        raise ValueError(f"Роль '{role}' не найдена в базе данных.")

    # Создаем пользователя
    user = User(username=username, email=email, password=password, role_id=role.id)
    session.add(user)
    await session.commit()

    return {"user_id": user.id}


@connection
async def create_user_with_profile(username: str,
                                   email: str,
                                   password: str,
                                   role: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        # Получаем роль из базы данных
        result = await session.execute(select(Role).where(Role.name == role))
        role = result.scalars().first()

        if role is None:
            raise ValueError(f"Роль '{role}' не найдена в базе данных.")

        user = User(username=username, email=email, password=password, role_id=role.id)
        session.add(user)
        await session.flush()  # Промежуточный шаг для получения user.id без коммита

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            contacts=contacts
        )
        session.add(profile)

        # Один коммит для обоих действий
        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()  # Откатываем транзакцию при ошибке
        raise e

@connection
async def create_user_example_4(users_data: List[dict], session: AsyncSession) -> List[int]:
    """
    Создает нескольких пользователей с использованием ORM SQLAlchemy.

    Аргументы:
    - users_data: list[dict] - список словарей, содержащих данные пользователей
      Каждый словарь должен содержать ключи: 'username', 'email', 'password'.
    - session: AsyncSession - асинхронная сессия базы данных

    Возвращает:
    - list[int] - список идентификаторов созданных пользователей
    """
    users_list = []
    for user in users_data:
        username = user['username']
        email = user['email']
        password = user['password']
        role_name = user['role']
        role = (await session.execute(select(Role).where(Role.name == role_name))).scalars().first()
        print(role)
        if role is None:
            raise ValueError(f"Роль '{role}' не найдена в базе данных.")
        role_id = role.id
        users_list.append(User(username=username, email=email, password=password, role_id=role_id))
    session.add_all(users_list)
    await session.commit()
    return [user.id for user in users_list]

if __name__ == '__main__':
    users = [
        {"username": "michael_brown", "email": "michael.brown@example.com", "password": "pass1234", 'role':'администратор'},
        {"username": "sarah_wilson", "email": "sarah.wilson@example.com", "password": "mysecurepwd", 'role':'администратор'},
        {"username": "david_clark", "email": "david.clark@example.com", "password": "davidsafe123", 'role':'администратор'},
        {"username": "emma_walker", "email": "emma.walker@example.com", "password": "walker987", 'role':'администратор'},
        {"username": "james_martin", "email": "james.martin@example.com", "password": "martinpass001", 'role':'пользователь'}
    ]
    result = run(create_user_example_4(users_data=users))
    print(result)
