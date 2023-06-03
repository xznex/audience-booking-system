from database import Base

from sqlalchemy import Column, Integer, String, Text, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
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

    id = Column(Integer, primary_key=True)
    audience = Column(String(10))
    event = Column(Text)
    day_of_week = Column(ChoiceType(choices=DAY_OF_WEEK))
    parity = Column(ChoiceType(choices=PARITY))
    start_of_class = Column(Time)
    end_of_class = Column(Time)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship('User', back_populates='audiences')

    def __repr__(self):
        return f"<Audience {self.id}>"
