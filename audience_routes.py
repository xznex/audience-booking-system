import re

from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from database import Session, engine
from models import User, Audience


audience_router = APIRouter(
    prefix="/audiences",
    tags=["audiences"]
)

session = Session(bind=engine)


def convert_to_latin(aud: str) -> str | None:
    aud = aud.upper()
    out = None
    if re.search(r"LK-\d\d\d$", aud):
        out = "ЛК" + aud[2:]
    elif re.search(r"A-\d\d\d$", aud):
        out = "А" + aud[2:]
    elif re.search(r"U-\d\d\d$", aud):
        out = "У" + aud[2:]
    elif re.search(r"PA-\d\d$", aud):
        out = "ПА" + aud[2:]
    return out


@audience_router.get("/audience/{audience}")
async def retrieve_an_audience(audience: str):
    formatted_audience = convert_to_latin(audience)
    if formatted_audience:
        inf = session.query(Audience).filter(Audience.audience == formatted_audience).all()
        # print(inf)
        return jsonable_encoder(inf)

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
