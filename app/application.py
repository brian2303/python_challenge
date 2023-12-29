import os
import graphene
from flask import Flask, request, Response, jsonify
from flask_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.infrastructure.router.book_router import GetBooks, MyMutations
from app.domain.usecase.create_user_use_case import CreateUserUseCase
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

app = Flask(__name__)


class AuthenticatedGraphQLView(GraphQLView):

    def dispatch_request(self):
        verify_jwt_in_request()
        return super(AuthenticatedGraphQLView, self).dispatch_request()


schema = graphene.Schema(query=GetBooks, mutation=MyMutations)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

app.add_url_rule(
    '/books',
    view_func=AuthenticatedGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        executor=AsyncioExecutor()
    )
)


@app.route('/login', methods=['POST'])
async def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        create_user_use_case = CreateUserUseCase()
        access_token = await create_user_use_case.check_user(username, password)
        return jsonify(access_token=access_token), 200
    except FileNotFoundError as error:
        return jsonify(error="Invalid credentials"), 401


@app.route('/create-user', methods=['POST'])
async def create_user():
    create_user_use_case = CreateUserUseCase()
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    try:
        data = await create_user_use_case.create_user(username, password)
        return jsonify(succesfully=data), 200
    except:
        return jsonify(succesfully="User already exists"), 500
