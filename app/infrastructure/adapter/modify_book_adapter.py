import os
import asyncio
import logging

from app.domain.model.book_model import Book
from app.infrastructure.external.mongo_db.dto_model.book_dto import BookDTO
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.external.requests.resource_type import ResourceType
from app.infrastructure.port.in_.modify_books_port import ModifyBooksPort
from app.infrastructure.external.requests.request_provider import RequestsProvider
from app.app_utils import AppUtils
from dotenv import load_dotenv


class ModifyBookAdapter(ModifyBooksPort):
    AppUtils.log_conf()
    load_dotenv()
    OPEN_API_ID = 'isbn'
    FIRST_ID = 0

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.google_api = os.getenv("GOOGLE_API")
        self.open_library_api = os.getenv("OPEN_LIBRARY_BOOK")
        self.mongo_provider = MongoProvider(self.collection)
        self.request_provider = RequestsProvider()

    async def insert_book(self, book_list):
        books = [self.__map_to_book_model(book) for book in book_list]
        response = await self.mongo_provider.insert(books)
        logging.info("get db  async data successfully")
        return response

    async def get_external_data(self, param):
        google_api_param, open_library_param = self.__build_params_to_requests(param)
        request_response = await asyncio.gather(self.request_provider.get_request(google_api_param, self.google_api),
                                                self.request_provider.get_request(open_library_param,
                                                                                  self.open_library_api))
        built_books = self.__extract_book_id(request_response)
        logging.info("get request  async data successfully")
        return built_books

    def __extract_book_id(self, request_response):
        raw_google_books_items = request_response[0].get('items', [])
        raw_open_library_items = request_response[1].get('docs', [])
        google_books_items = [Book(
            id=book.get("id"),
            resource=ResourceType.GOOGLE_API.value
        ) for book in raw_google_books_items]

        open_library_items = [Book(
            id=book.get(self.OPEN_API_ID)[self.FIRST_ID],
            resource=ResourceType.OPEN_LIBRARY_API.value
        ) for book in raw_open_library_items if len(book) != 0]
        return google_books_items + open_library_items

    def __build_params_to_requests(self, param):
        google_api_param = {'q': param}
        open_library_api_param = {'q': param, 'fields': self.OPEN_API_ID}
        return google_api_param, open_library_api_param

    @classmethod
    def __map_to_book_model(cls, request_response):
        return BookDTO(
            id=request_response.get("id"),
            title=request_response.get("volumeInfo").get("title"),
            subtitle=request_response.get("volumeInfo").get("subtitle"),
            authors=request_response.get("volumeInfo").get("authors"),
            categories=request_response.get("volumeInfo").get("categories"),
            published_date=request_response.get("volumeInfo").get("publishedDate"),
            editor=request_response.get("volumeInfo").get("publisher"),
            description=request_response.get("volumeInfo").get("description"),
            image=request_response.get("volumeInfo").get("imageLinks").get("large")
        ).model_dump_json()
