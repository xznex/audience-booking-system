from database import Base

from sqlalchemy import Column, Integer, String, Text, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    audiences = relationship("Audience", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Audience(Base):
    __tablename__ = "audience"

    DAY_OF_WEEK = (
        ("ПОНЕДЕЛЬНИК", "Понедельник"),
        ("ВТОРНИК", "Вторник"),
        ("СРЕДА", "Среда"),
        ("ЧЕТВЕРГ", "Четверг"),
        ("ПЯТНИЦА", "Пятница"),
        ("СУББОТА", "Суббота"),
    )

    PARITY = (
        ("чёт", "Чётная"),
        ("нечёт", "Нечётная")
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    audience: Mapped[str] = mapped_column(
        String(length=10), nullable=True
    )
    event: Mapped[str] = mapped_column(
        String, nullable=False
    )
    day_of_week = Column(ChoiceType(choices=DAY_OF_WEEK))
    parity = Column(ChoiceType(choices=PARITY))
    start_of_class = Column(Time)
    end_of_class = Column(Time)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship('User', back_populates='audiences')

    def __repr__(self):
        return f"<Audience {self.id}>"
