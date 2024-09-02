from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM
import python_jwt as jwt
from strawberry.permission import BasePermission
from strawberry.types import Info
import typing


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_password_hashed(pwd):
    return pwd_context.hash(pwd)

class JWTManager:

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt._JWTError:
            raise Exception("Invalid token")


class IsAuthenticated(BasePermission):
    msg = "User is not Authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        req = info.context["request"]
        # Access headers authentication
        auth = req.headers["authentication"]
        if auth:
            token = auth.split("Bearer ")[-1]
            return JWTManager.decode_token(token)
        return False