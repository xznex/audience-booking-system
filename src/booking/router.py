import os
import re
import sys

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

# from src.database import get_async_session, engine
# from models import Audience

# sys.path.append(os.path.join(sys.path[0], 'src'))
from src.booking.models import Audience
from src.database import get_async_session

audience_router = APIRouter(
    prefix="/audiences",
    tags=["audiences"]
)


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


# @audience_router.get("/audience/{audience}")
# async def retrieve_an_audience(audience: str):
#     formatted_audience = convert_to_latin(audience)
#     if formatted_audience:
#         inf = session.query(Audience).filter(Audience.audience == formatted_audience).limit(10)
#         # print(inf)
#         return jsonable_encoder(inf)
#
#     raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

@audience_router.get("/audience/{audience}")
async def retrieve_an_audience(audience: str, session: AsyncSession = Depends(get_async_session)):
    formatted_audience = convert_to_latin(audience)
    if formatted_audience:
        query = session.query(Audience).filter(Audience.audience == formatted_audience).limit(10)
        result = await session.execute(query)
        return result.all()
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
