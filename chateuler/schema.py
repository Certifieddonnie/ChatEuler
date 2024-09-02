import strawberry
from strawberry.types import Info
from config import db
# from strawberry.fastapi import GraphQLRouter
from utils import JWTManager, get_password_hashed, verify_password, IsAuthenticated
from model.user import User
from sqlalchemy.future import select


@strawberry.type
class UserType:
    user_id: str
    username: str


async def get_db():
    async with db as session:
        yield session


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def current_user(self, info: Info) -> UserType:
        async with db as session:
            token = info.context["request"].headers.get("Authorization")
            if not token:
                return None
            token_data = JWTManager.decode_token(token)
            user = await session.get(User, token_data["user_id"])
            if user:
                return UserType(id=str(user.user_id), username=user.username)
            return None
    
    @strawberry.field
    def home(self) -> str:
        return "Welcome to CHATEULER!"

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, username: str, password: str, info: Info) -> UserType:
        async with db as session:
            hashed_password = get_password_hashed(password)
            db_user = User(username=username, hashed_password=hashed_password)
            session.add(db_user)
            await db.commit_rollback()
            return UserType(id=str(db_user.user_id), username=db_user.username)
    
    @strawberry.mutation
    async def login(self, username: str, password: str, info: Info) -> str:
        async with db as session:
            user = await session.execute(
                select(User).where(User.username == username)
            )
            user = user.scalars().first()
            if not user or not verify_password(password, user.hashed_password):
                raise Exception("Invalid credentials")
            token = JWTManager.create_access_token({"user_id": str(user.user_id)})
            return token
