import strawberry
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config import DatabaseSession
from strawberry.asgi import GraphQL
from schema import Query, Mutation

def init_app():
    db = DatabaseSession()
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
    
    # graphql endpoint
    schema = strawberry.Schema(query=Query, mutation=Mutation)

    graphql_app = GraphQL(schema)

    app.add_route("/graphql", graphql_app)
    app.add_websocket_route("/graphql", graphql_app)


    
    return apps

app = init_app()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='localhost', port=8080, reload=True)