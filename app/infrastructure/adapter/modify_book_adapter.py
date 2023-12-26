import os
import asyncio
from app.infrastructure.external.mongo_db.dto_model.book_dto import BookDTO
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.port.in_.modify_books_port import ModifyBooksPort
from app.infrastructure.external.requests.request_provider import RequestsProvider


class ModifyBookAdapter(ModifyBooksPort):

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.url = os.getenv("URL")
        self.mongo_provider = MongoProvider(self.collection)
        self.request_provider = RequestsProvider(self.url)

    def insert_book(self, book):
        response = asyncio.run(self.mongo_provider.insert(book.model_dump_json()))
        return response

    def get_external_data(self, param):
        request_response = self.request_provider.get_request(param)
        return BookDTO(**request_response)
