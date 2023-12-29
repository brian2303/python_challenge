import logging

from app.infrastructure.adapter.modify_book_adapter import ModifyBookAdapter
from app.infrastructure.adapter.find_book_adapter import FindBookAdapter
from app.app_utils import AppUtils


class BookManageUseCase:
    AppUtils.log_conf()

    def __init__(self):
        self.modify_book = ModifyBookAdapter()
        self.process_book = FindBookAdapter()

    async def find_book_criteria(self, find_criteria):
        return await self.process_book.find_book(find_criteria)

    async def process_book_data(self, find_criteria):
        try:
            book = await self.find_book_criteria(find_criteria)
            if len(book) == 0:
                book_founded = await self.modify_book.get_all_external_data(find_criteria)
                return book_founded
            return book
        except Exception as error:
            logging.error(str(error))



    async def delete_book(self, book_id):
        return await self.modify_book.delete_book_by_id(book_id)
