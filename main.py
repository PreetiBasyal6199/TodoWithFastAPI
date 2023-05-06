import uvicorn
from fastapi import FastAPI
from app.views import router as AppRouter

app = FastAPI()

app.include_router(AppRouter)


@app.get("/", tags=["Root"])
def start():
    return {"Hello": "World"}
