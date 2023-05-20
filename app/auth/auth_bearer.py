import time
from typing import Dict
import jwt
from decouple import config
from passlib.context import CryptContext
from app.database import user_collection

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def token_response(token: str):
    return {
        'access': token
    }


# Function used for signing the JWT String
def signJWT(userEmail: str):
    payload = {
        "email": userEmail,
        "expires_at": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires_at"] >= time.time() else None
    except:
        return {}


# Function to fetch the user_id
def get_user_id(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = decoded_token.get("email")
        user_obj = user_collection.find_one({"email": email})
        return user_obj['_id']
    except:
        return {}


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hasher:
    @staticmethod
    def hash_password(plain_password: str):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)
