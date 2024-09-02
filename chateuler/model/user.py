from uuid import uuid4, UUID as UUIDType
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """ User Model """
    __tablename__ = "users"
    
    user_id: Optional[UUIDType] = Field(default_factory=uuid4, primary_key=True, nullable=False, sa_column=Column(SA_UUID(as_uuid=True), default=uuid4, unique=True, index=True))
    username: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
