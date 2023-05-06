from .models import UserPostSchema, UserLoginSchema
from app.auth.auth_bearer import signJWT, decodeJWT, Hasher
# from main import app
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from .database import user_collection
from .helpers import userhelper

router = APIRouter()


@router.post("/user/signup/", tags=["User"])
def create_user(user: UserPostSchema = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = Hasher.hash_password(user.pop("password"))
    user_collection.insert_one(user)
    return userhelper(user)


@router.post("/user/login/", tags=["User"])
def login_user(user: UserLoginSchema = Body(...)):
    user = jsonable_encoder(user)
    current_user = user_collection.find_one({'email': user['email']})
    if current_user:
        if Hasher.verify_password(user['password'], current_user['password']):
            return signJWT(current_user['email'])
    else:
        return {
            "detail": "Invalid Credentials."
        }
