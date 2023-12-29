import logging

from app.app_utils import AppUtils
from app.infrastructure.adapter.create_book_adapter import CreateBookAdapter
from app.domain.usecase.book_manage_use_case import BookManageUseCase


class CreateBookUseCase:
    AppUtils.log_conf()

    def __init__(self):
        self.create_book = CreateBookAdapter()
        self.book_manage_use_case = BookManageUseCase()

    async def save_book(self, raw_book_data):
        book_found = await self.book_manage_use_case.find_book_criteria(raw_book_data.id)
        if len(book_found) > 0:
            raise FileExistsError
        book_response = await self.create_book.insert_data_from_external_requests(raw_book_data)
        return book_response
