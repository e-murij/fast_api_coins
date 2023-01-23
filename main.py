from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import dictionary, coin, user

from config import settings
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dictionary.router, tags=['Dict'], prefix='/api/dictionary')
app.include_router(coin.router, tags=['Coins'], prefix='/api/coins')
app.include_router(user.router, tags=['User'], prefix='/api/user')


@app.get("/")
def read_root():
    return {"Hello": "User"}
