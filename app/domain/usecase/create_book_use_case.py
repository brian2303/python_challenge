import logging

from app.infrastructure.adapter.create_book_adapter import CreateBookAdapter
from app.domain.usecase.find_book_use_case import FindBookUseCase


class CreateBookUseCase:

    def __init__(self):
        self.create_book = CreateBookAdapter()
        self.find_book_use_case = FindBookUseCase()

    async def save_book(self, raw_book_data):
        book_found = await self.find_book_use_case.find_book_criteria(raw_book_data.id)
        if len(book_found) > 0:
            logging.info(f"Book with id {raw_book_data.id} not found")
            raise FileExistsError
        book_response = await self.create_book.insert_data_from_external_requests(raw_book_data)
        return book_response
