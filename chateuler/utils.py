from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM
import python_jwt as jwt
from strawberry.permission import BasePermission
from strawberry.types import Info
import typing


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_password_hashed(pwd: str) -> str:
    return pwd_context.hash(pwd)

class JWTManager:

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # Use timezone-aware datetime
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt._JWTError as e:
            raise Exception("Invalid token") from e


class IsAuthenticated(BasePermission):
    msg = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        req = info.context["request"]
        auth_header = req.headers.get("Authorization")  # Use "Authorization" header key
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[-1]
            try:
                JWTManager.decode_token(token)
                return True
            except Exception:
                return False
        return False
