from app.infrastructure.adapter.delete_book_adapter import DeleteBookAdapter

from app.app_utils import AppUtils


class DeleteBookUseCase:
    AppUtils.log_conf()

    def __init__(self):
        self.delete_book = DeleteBookAdapter()

    async def delete_book_by_id(self, book_id):
        return await self.delete_book.delete_book_by_id(book_id)
