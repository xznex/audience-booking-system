from database import engine, Base
from models import User, Audience


Base.metadata.create_all(bind=engine)
