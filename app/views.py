import json

import jwt

from .models import UserPostSchema, UserLoginSchema, TodoPostSchema, TodoUpdateSchema
from app.auth.auth_bearer import signJWT, decodeJWT, Hasher, get_user_id
from app.auth.auth_handler import JWTBearer
from bson import ObjectId
from fastapi.responses import JSONResponse  # from main import app
from fastapi import APIRouter, Body, Depends, HTTPException
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


@router.get("/todos/", dependencies=[Depends(JWTBearer())], tags=["Todos"])
def my_todos(token: str = Depends(JWTBearer())):
    user_id = get_user_id(token)
    my_todos = todo_collection.find_one({"user_id": ObjectId(user_id)})
    if my_todos:
        return todohelper(my_todos)
    return {}


@router.patch("/todo/{todo_id}/")
def update_todo(todo_id: str, todo: TodoUpdateSchema = Body(None), token: str = Depends(JWTBearer())):
    todo_obj = todo_collection.find_one({"_id": ObjectId(todo_id)})
    user_id = get_user_id(token)
    if todo_obj["user_id"] != user_id:
        raise ValueError("You are not allowed to update this todo.")
    updated_todo = todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": todo.dict()})
    return JSONResponse({"message": "Successfully updated "})


@router.delete("/todo/{todo_id}/")
def delete_todo(todo_id: str, token: str = Depends(JWTBearer())):
    todo_obj = todo_collection.find_one({"_id": ObjectId(todo_id)})
    user_id = get_user_id(token)
    if todo_obj["user_id"] != user_id:
        raise HTTPException(403, detail="You are not allowed to update this todo.")
    todo_collection.delete_one({"_id": ObjectId(todo_id)})
    return JSONResponse({"message": "Todo deleted"}, 204)
