import os
import logging

from app.infrastructure.port.in_.create_book_port import CreateBooksPort
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.external.common.resource_type import ResourceType
from app.infrastructure.adapter.find_book_adapter import FindBookAdapter


class CreateBookAdapter(CreateBooksPort):
    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.find_book_adapter = FindBookAdapter()
        self.mongo_provider = MongoProvider(self.collection)

    async def insert_data_from_external_requests(self, raw_data_book):
        request_book_callable = self.__resource_type_selector_by_id().get(raw_data_book.resource)
        book = await request_book_callable(raw_data_book.id)
        await self.insert_book(book)
        return book

    async def insert_book(self, book):
        response = await self.mongo_provider.insert(book)
        logging.info("get db  async data successfully")
        return response

    def __resource_type_selector_by_id(self):
        return {
            ResourceType.GOOGLE_API.value: self.find_book_adapter.search_book_google_api_by_id,
            ResourceType.OPEN_LIBRARY_API.value: self.find_book_adapter.search_book_open_library_api_by_id
        }
