import os
from dotenv import load_dotenv

from app.infrastructure.external.mongo_db.dto_model.book_dto import BookDTO
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider
from app.infrastructure.port.out.process_books_port import ProcessBooksPort


class ProcessBookAdapter(ProcessBooksPort):
    load_dotenv()

    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.mongo_provider = MongoProvider(self.collection)

    async def find_book(self, query):
        response = await self.mongo_provider.find_one(query)
        if response is not None:
            return BookDTO(**response)
        return response
