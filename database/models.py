from sqlalchemy import ForeignKey, text, ARRAY, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from database.database import Base, uniq_str_an
from database.sql_enums import GenderEnum, ProfessionEnum, StatusPostEnum, RatingEnum


class User(Base):
    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profiles.id"))

    # One-to-one with Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Ключевой параметр для связи один-к-одному
        lazy="joined"  # Автоматически подгружает profile при запросе user
    )
    # One-to-many with Posts
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )
    # One-to-many with Comments
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Comment
    )


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        # server_default=text("UNEMPLOYED")
    )
    interests: Mapped[List[str] | None] = mapped_column(JSON)
    contacts: Mapped[dict | None] = mapped_column(JSON)

    # Back One-to-one with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )


class Post(Base):
    title: Mapped[str]
    content: Mapped[str] =  mapped_column(Text)
    main_photo_url: Mapped[str]
    photos_url: Mapped[List[str] | None] = mapped_column(JSON)
    status: Mapped[StatusPostEnum] = mapped_column(default=StatusPostEnum.PUBLISHED, server_default=text("'DRAFT'"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Many-to-one with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
    # One-to-many with Comments
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] =  mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))

    # Many-to-one with Post
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
    )
    # Many-to-one with User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments",
    )