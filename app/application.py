import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.infrastructure.router.book_router import BookRouter


app = Flask(__name__)

app.add_url_rule(
    '/books',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=graphene.Schema(query=BookRouter),
        graphiql=True,
        executor=AsyncioExecutor()
    )
)
