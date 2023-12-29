import os
import asyncio
import logging

from app.infrastructure.router.models.book_model import Book
from app.domain.model.book_dto import BookDTO
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.external.common.resource_type import ResourceType
from app.infrastructure.port.in_.modify_books_port import ModifyBooksPort
from app.infrastructure.external.requests.request_provider import RequestsProvider
from app.app_utils import AppUtils
from dotenv import load_dotenv


class ModifyBookAdapter(ModifyBooksPort):
    AppUtils.log_conf()
    load_dotenv()
    OPEN_API_ID = 'isbn'
    FIRST_ID = 0
    PARAM_NAME = "fields"
    STR_FIELDS = "isbn,title,author_name,subject_key,publish_date"

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.google_api = os.getenv("GOOGLE_API")
        self.open_library_api = os.getenv("OPEN_LIBRARY_BOOK")
        self.mongo_provider = MongoProvider(self.collection)
        self.request_provider = RequestsProvider()

    async def get_all_external_data(self, param):
        request_response = await asyncio.gather(self.__get_books_by_google_api(param),
                                                self.__get_books_by_open_library_api(param))
        built_books = self.__map_book_to_model(request_response)
        logging.info("get request  async data successfully")
        return built_books

    def __map_book_to_model(self, request_response):
        raw_google_books_items = request_response[0]
        raw_open_library_items = request_response[1]
        google_books_items = [Book(
            id=book.get("id"),
            resource=ResourceType.GOOGLE_API.value,
            title=book.get("title"),
            subtitle=book.get("subtitle"),
            categories=book.get("categories")
        ) for book in raw_google_books_items]

        open_library_items = [Book(
            id=book.get("id"),
            resource=ResourceType.OPEN_LIBRARY_API.value,
            title=book.get("title"),
            subtitle=book.get("subtitle"),
            categories=book.get("categories")
        ) for book in raw_open_library_items if len(book) != 0]
        return google_books_items + open_library_items

    def __build_params_to_requests(self, param):
        format_param = param.strip()
        format_param = format_param.replace(" ", "+")
        google_api_param = {'q': format_param}
        open_library_api_param = {'q': format_param, self.PARAM_NAME: self.STR_FIELDS}
        return google_api_param, open_library_api_param

    async def __get_books_by_google_api(self, search):
        google_api_param, open_library_api_param = self.__build_params_to_requests(search)
        book_list = await self.request_provider.get_request(google_api_param, self.google_api)
        books = book_list.get("items", [])
        return [self.__map_to_google_book_model(book) for book in books]

    async def __get_books_by_open_library_api(self, search):
        google_api_param, open_library_api_param = self.__build_params_to_requests(search)
        book_list = await self.request_provider.get_request(open_library_api_param, self.open_library_api)
        books = book_list.get("docs", [])
        return [self.__map_to_open_library_book_model(book) for book in books]
