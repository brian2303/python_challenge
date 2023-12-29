import os
import logging

from app.infrastructure.port.in_.delete_book_port import DeleteBookPort
from app.infrastructure.external.mongo_db.mongo_provider import MongoProvider


class DeleteBookAdapter(DeleteBookPort):
    def __init__(self):
        self.collection = os.getenv("COLLECTION")
        self.mongo_provider = MongoProvider(self.collection)

    async def delete_book_by_id(self, book_id):
        book_found = await self.mongo_provider.delete_by_id(book_id)
        logging.info("Book deleted successfully")
        return book_found.acknowledged
