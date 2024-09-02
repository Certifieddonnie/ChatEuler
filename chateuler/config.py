import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = os.getenv('DB_CONFIG')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

class DatabaseSession:
    def __init__(self,url:str=DB_CONFIG):
        self.engine = create_async_engine(url,echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    #It generates models into a database
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    
    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
    
    # Close connection
    async def close(self):
        await self.engine.dispose()
    
    # Prepare the context for the async ops
    async def __center__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session
    
    # it is used to clean up resources
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

db = DatabaseSession()