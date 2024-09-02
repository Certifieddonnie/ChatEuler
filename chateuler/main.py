import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config import db

def init_app():
    apps = FastAPI(
        title="Chat Euler",
        description="Fast API Chatbot",
        version="1.0.0"
    )
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.create_all()
        yield
        await db.close()

    @apps.get('/')
    def home():
        return "Welcome Home"
    
    return apps

app = init_app()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='localhost', port=8080, reload=True)