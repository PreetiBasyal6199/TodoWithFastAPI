from .models import UserPostSchema, UserLoginSchema
from app.auth.auth_bearer import signJWT, decodeJWT
# from main import app
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from .database import user_collection
from .helpers import userhelper

router = APIRouter()


@router.post("/user/", tags=["User"])
def create_user(user: UserPostSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = user_collection.insert_one(user)
    return userhelper(user)
