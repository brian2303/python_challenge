from graphene import String, Mutation, ID, Boolean
from app.domain.usecase.delete_book_use_case import DeleteBookUseCase


class DeleteBook(Mutation):
    class Arguments:
        book_id = ID(required=True)

    success = Boolean()
    message = String()

    async def mutate(self, info, book_id):
        try:
            delete_book_use_case = DeleteBookUseCase()
            delete_success = await delete_book_use_case.delete_book_by_id(book_id)
            return DeleteBook(success=delete_success,
                              message="Delete book with id {} successfully".format(book_id))
        except FileNotFoundError:
            return DeleteBook(success=False,
                              message="Book not found")
