from app.infrastructure.adapter.delete_book_adapter import DeleteBookAdapter


class DeleteBookUseCase:

    def __init__(self):
        self.delete_book = DeleteBookAdapter()

    async def delete_book_by_id(self, book_id):
        return await self.delete_book.delete_book_by_id(book_id)
