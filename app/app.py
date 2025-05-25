from typing import Union
from mangum import Mangum
from fastapi.responses import JSONResponse
import uvicorn
from typing import Union
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud
from .database import engine, SessionLocal, Base

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def read_root():
   return {"Welcome to": "My first FastAPI deployment using Docker image"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
   return JSONResponse({"item_id": item_id, "q": q})

@app.get('/test/{int}')
def square(int: int):
   return int ** 2

@app.get('/info')
def info():
   return JSONResponse({"info": """India is a land of various cultures and a rich heritage.It is
                        the seventh-largest country by area and the second-most populous country 
                        globally. The peacock is India's national bird, and the Bengal tiger is the
                        country's national animal. The national song is named Vande Matram (written by Bankimchandra Chatterji)."""})





# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)


if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)