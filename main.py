from fastapi import FastAPI

from audience_routes import audience_router


app = FastAPI()


app.include_router(audience_router)
