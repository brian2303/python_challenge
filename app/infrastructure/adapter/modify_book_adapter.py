import os
import asyncio
import logging

from app.domain.model.book_model import Book
from app.infrastructure.external.mongo_db.dto_model.book_dto import BookDTO
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
    STR_FIELDS = "title,author_name,subject_key,publish_date"

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.google_api = os.getenv("GOOGLE_API")
        self.open_library_api = os.getenv("OPEN_LIBRARY_BOOK")
        self.mongo_provider = MongoProvider(self.collection)
        self.request_provider = RequestsProvider()

    async def insert_book(self, book):
        response = await self.mongo_provider.insert(book)
        logging.info("get db  async data successfully")
        return response

    async def get_all_external_data(self, param):
        google_api_param, open_library_param = self.__build_params_to_requests(param)
        request_response = await asyncio.gather(self.request_provider.get_request(google_api_param, self.google_api),
                                                self.request_provider.get_request(open_library_param,
                                                                                  self.open_library_api))
        built_books = self.__extract_book_id(request_response)
        logging.info("get request  async data successfully")
        return built_books

    async def insert_data_from_external_requests(self, raw_data_book):
        request_book_callable = self.__resource_type_selector().get(raw_data_book.resource)
        book = await request_book_callable(raw_data_book.id)
        await self.insert_book(book)
        return book

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
        format_param = param.strip()
        format_param = format_param.replace(" ", "+")
        google_api_param = {'q': format_param}
        open_library_api_param = {'q': format_param, self.PARAM_NAME: self.OPEN_API_ID}
        return google_api_param, open_library_api_param

    def __resource_type_selector(self):
        return {
            ResourceType.GOOGLE_API.value: self.__get_books_by_google_api,
            ResourceType.OPEN_LIBRARY_API.value: self.__get_books_by_open_library_api
        }

    async def __get_books_by_google_api(self, id):
        id_param = {'q': id}
        book_list = await self.request_provider.get_request(id_param, self.google_api)
        books = book_list.get("items", [])
        return [self.__map_to_google_book_model(book) for book in books][self.FIRST_ID]

    async def __get_books_by_open_library_api(self, id):
        id_param = {'q': id,
                    self.PARAM_NAME: self.STR_FIELDS}
        book_list = await self.request_provider.get_request(id_param, self.open_library_api)
        books = book_list.get("docs", [])
        return [self.__map_to_open_library_book_model(id, book) for book
                in books if len(books) != 0][self.FIRST_ID]

    @classmethod
    def __map_to_google_book_model(cls, request_response):
        return BookDTO(
            id=request_response.get("id"),
            title=request_response.get("volumeInfo").get("title"),
            subtitle=request_response.get("volumeInfo").get("subtitle", ""),
            authors=request_response.get("volumeInfo").get("authors"),
            categories=request_response.get("volumeInfo").get("categories"),
            published_date=request_response.get("volumeInfo").get("publishedDate"),
            editor=request_response.get("volumeInfo").get("publisher"),
            description=request_response.get("volumeInfo").get("description"),
            image=request_response.get("volumeInfo").get("imageLinks").get("large", "")
        ).model_dump()

    def __map_to_open_library_book_model(self, id, request_response):
        return BookDTO(
            id=id,
            title=request_response.get("title"),
            subtitle="",
            authors=request_response.get("author_name"),
            categories=request_response.get("subject_key"),
            published_date=request_response.get("publish_date")[self.FIRST_ID],
            editor="",
            description="",
            image=""
        ).model_dump()
