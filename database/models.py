from email.policy import default

from sqlalchemy import ForeignKey, text, ARRAY, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from database.db import Base, uniq_str_an
from database.sql_enums import GenderEnum, ProfessionEnum, RoleEnum, DiagnosesEnum


# Structure of a database
# 1. Users
# 2. Patients
# 3. Roles
# 5. Profiles
# 6. Hospital

# Define User class (User is a person, who can work with service)
class User(Base):
    # Basic variables
    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]  # Needs to be encrypted in future

    # Foreign keys
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))

    # Relations
    # One-to-one with Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Ключевой параметр для связи один-к-одному
        lazy="joined"  # Автоматически подгружает profile при запросе user
    )
    # One-to-one with Role
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user",
        uselist=False,
        lazy="joined"
    )


class Profile(Base):
    # Basic values
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum | None]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    contacts: Mapped[dict | None] = mapped_column(JSON)

    # Foreign keys
    ...

    # Relations
    # Back One-to-one with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )


class Patient(Base):
    # Basic values
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    contacts: Mapped[dict | None] = mapped_column(JSON)
    diagnosis: Mapped[DiagnosesEnum] = mapped_column(
        default=DiagnosesEnum.HEALTHY,
        server_default=text("'HEALTHY'")
    )

    # Foreign keys
    hospital_id: Mapped[int] = mapped_column(ForeignKey("hospitals.id"))

    # Relations
    # Many-to-one with Hospital
    hospital: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="patient",
        uselist=False,
        lazy="joined"
    )


class Hospital(Base):
    # Basic values
    name: Mapped[uniq_str_an]
    address: Mapped[uniq_str_an | None]

    # Foreign keys
    ...

    # Relations
    patients: Mapped[list["Patient"]] = relationship(
        "Patient",
        back_populates="hospital",
        lazy="joined"
    )


class Role(Base):
    # Basic values
    name: Mapped[RoleEnum] = mapped_column(default=RoleEnum.USER, server_default=text("'USER'"))

    # Foreign keys
    ...

    # Relations
    # Back One-to-one with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="role",
        uselist=False,
    )
