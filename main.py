from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def index():
    return {
        "message": "This API on EC2,OK"
    }

@app.post("/add")
async def add(a: int,b: int):
    return a+b