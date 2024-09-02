from uuid import uuid4, UUID
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from sqlmodel import SQLModel
from pydantic import Field, RootModel


class User(SQLModel, table=True):
    """ User Model """
    __tablename__ = "users"
    
    user_id: str
    username: str
    hashed_password: str
