import os
from dotenv import load_dotenv

from app.domain.model.book_model import Book
from app.infrastructure.external.common.resource_type import ResourceType
from app.infrastructure.external.mongo_db.dto_model.book_dto import BookDTO
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.port.out.process_books_port import ProcessBooksPort


class ProcessBookAdapter(ProcessBooksPort):
    load_dotenv()

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.mongo_provider = MongoProvider(self.collection)

    async def find_book(self, query):
        response = await self.mongo_provider.find_books(query)
        if response is not None:
            return [Book(
                id=book.get("id"),
                resource=ResourceType.INTERNAL_DB.value
            ) for book in response]
        return response
