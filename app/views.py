import jwt

from .models import UserPostSchema, UserLoginSchema, TodoPostSchema
from app.auth.auth_bearer import signJWT, decodeJWT, Hasher, get_user_id
from app.auth.auth_handler import JWTBearer
# from main import app
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from .database import user_collection, todo_collection
from .helpers import userhelper, todohelper

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


@router.post("/todo/", dependencies=[Depends(JWTBearer())], tags=["Todos"])
def create_todo(todo: TodoPostSchema = Body(...), token: str = Depends(JWTBearer())):
    todo_obj = jsonable_encoder(todo)
    user_id = get_user_id(token=token)
    todo_obj['user_id'] = user_id
    todo_collection.insert_one(todo_obj)
    return todohelper(todo_obj)
