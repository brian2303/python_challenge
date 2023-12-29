import logging

from app.infrastructure.adapter.find_book_adapter import FindBookAdapter


class FindBookUseCase:

    def __init__(self):
        self.find_book_adapter = FindBookAdapter()

    async def process_book_data(self, find_criteria):
        try:
            book = await self.find_book_criteria(find_criteria)
            if len(book) == 0:
                book_founded = await self.find_book_adapter.get_all_external_data(find_criteria)
                return book_founded
            return book
        except Exception as error:
            logging.error(str(error))

    async def find_book_criteria(self, find_criteria):
        return await self.find_book_adapter.find_book(find_criteria)
