import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.infrastructure.router.book_router import GetBooks, MyMutations

app = Flask(__name__)

schema = graphene.Schema(query=GetBooks, mutation=MyMutations)

app.add_url_rule(
    '/books',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        executor=AsyncioExecutor()
    )
)
