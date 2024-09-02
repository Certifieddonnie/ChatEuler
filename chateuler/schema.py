import strawberry
from strawberry.types import Info
from config import db
# from strawberry.fastapi import GraphQLRouter
from utils import JWTManager, get_password_hashed, verify_password, IsAuthenticated
from model.user import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

@strawberry.type
class UserType:
    user_id: str
    username: str

async def get_db() -> AsyncSession:
    async with db() as session:
        yield session

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def current_user(self, info: Info, db: AsyncSession = Depends(get_db)) -> UserType:
        token = info.context["request"].headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=403, detail="Authorization token missing")
        
        token_data = JWTManager.decode_token(token)
        user = await db.get(User, token_data["user_id"])
        
        if user:
            return UserType(user_id=str(user.user_id), username=user.username)
        return None
    
    @strawberry.field
    def home(self) -> str:
        return "Welcome to CHATEULER!"

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, username: str, password: str, info: Info, db: AsyncSession = Depends(get_db)) -> UserType:
        hashed_password = get_password_hashed(password)
        db_user = User(username=username, hashed_password=hashed_password)
        db.add(db_user)
        
        try:
            await db.commit()
            await db.refresh(db_user)
        except Exception:
            await db.rollback()
            raise
        
        return UserType(user_id=str(db_user.user_id), username=db_user.username)
    
    @strawberry.mutation
    async def login(self, username: str, password: str, info: Info, db: AsyncSession = Depends(get_db)) -> str:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=403, detail="Invalid credentials")
        
        token = JWTManager.create_access_token({"user_id": str(user.user_id)})
        return token
