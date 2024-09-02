from uuid import uuid4, UUID
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """ User Model """
    __tablename__ = "users"
    
    user_id: Optional[int] = Field(None, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True)
    hashed_password: str
