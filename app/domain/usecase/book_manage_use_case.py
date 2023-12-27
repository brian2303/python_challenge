from app.infrastructure.adapter.modify_book_adapter import ModifyBookAdapter
from app.infrastructure.adapter.process_book_adapter import ProcessBookAdapter


class BookManageUseCase:

    def __init__(self):
        self.modify_book = ModifyBookAdapter()
        self.process_book = ProcessBookAdapter()

    async def process_book_data(self, find_criteria):
        book = await self.process_book.find_book(find_criteria)
        if book is None:
            ext_response = await self.modify_book.get_external_data(find_criteria)
            return ext_response
        return book

    async def save_book(self, founded_books):
        if len(founded_books) > 0:
            await self.modify_book.insert_book(founded_books)
