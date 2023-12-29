import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.infrastructure.port.in_.create_user_port import CreateUserPort
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider


class CreateUserAdapter(CreateUserPort):
    def __init__(self):
        self.collection = os.getenv("COLLECTION_USERS")
        self.mongo_provider = MongoProvider(self.collection)

    async def create_user(self, username, password):
        password_hash = generate_password_hash(password)
        user_document = {
            "username": username,
            "password_hash": password_hash
        }
        data = await self.mongo_provider.insert(user_document)
        return data.acknowledged

    async def check_user(self, username, password):
        user_document = await self.find_by_username(username)
        if user_document and check_password_hash(user_document["password_hash"], password):
            access_token = create_access_token(identity=username)
            return access_token
        raise FileNotFoundError

    async def find_by_username(self, username):
        return await self.mongo_provider.find_user_by_name(username)

