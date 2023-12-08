from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    return {
        "message": "This API on EC2,OK"
    }