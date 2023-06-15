from datetime import time

from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john",
                "email": "john@gmail.com",
                "password": "password",
                "is_staff": False,
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john",
                "password": "password",
            }
        }


class AudienceModel(BaseModel):
    id: Optional[int]
    audience: str
    event: str
    day_of_week: str
    parity: str
    start_of_class: time
    end_of_class: time
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "audience": "ПА-15",
                "event": "john@gmail.com",
                "day_of_week": "ВТОРНИК",
                "parity": "нечёт",
                "start_of_class": "18:50",
                "end_of_class": "20:20",
                "user_id": 1
            }
        }
