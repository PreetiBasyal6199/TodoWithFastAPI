import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Root"])
def start():
    return {"Hello": "World"}
