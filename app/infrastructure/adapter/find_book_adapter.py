import os
from dotenv import load_dotenv

from app.infrastructure.router.models.book_model import Book
from app.infrastructure.external.common.resource_type import ResourceType
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.external.requests.request_provider import RequestsProvider
from app.infrastructure.port.out.process_books_port import FindBooksPort
from app.infrastructure.utils.mapper import MapperUtils
from app.app_utils import AppUtils


class FindBookAdapter(FindBooksPort):
    load_dotenv()

    AppUtils.log_conf()
    load_dotenv()
    OPEN_API_ID = 'isbn'
    FIRST_ID = 0
    PARAM_NAME = "fields"
    STR_FIELDS = "isbn,title,author_name,subject_key,publish_date"

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.mongo_provider = MongoProvider(self.collection)
        self.google_api = os.getenv("GOOGLE_API")
        self.open_library_api = os.getenv("OPEN_LIBRARY_BOOK")
        self.request_provider = RequestsProvider()

    async def find_book(self, query):
        response = await self.mongo_provider.find_books(query)
        if response is not None:
            return [Book(
                id=book.get("id"),
                resource=ResourceType.INTERNAL_DB.value,
                title=book.get("title"),
                subtitle=book.get("subtitle")
            ) for book in response]
        return response

    async def search_book_google_api_by_id(self, book_id):
        full_url = f"{self.google_api}{book_id}"
        book_found = await self.request_provider.get_request(book_id, full_url)
        return MapperUtils.map_to_google_book_model(book_found)

    async def search_book_open_library_api_by_id(self, book_id):
        id_param = {'q': book_id,
                    self.PARAM_NAME: self.STR_FIELDS}
        book_list = await self.request_provider.get_request(id_param, self.open_library_api)
        books = book_list.get("docs", [])
        return [MapperUtils.map_to_open_library_book_model(book) for book in books][self.FIRST_ID]


