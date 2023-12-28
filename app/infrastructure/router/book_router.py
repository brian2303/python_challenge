from graphene import ObjectType, Field, List, String, Mutation, ID, Boolean

from app.domain.model.book_model import Book
from app.domain.model.save_book_response import SaveBookResponse
from app.domain.usecase.book_manage_use_case import BookManageUseCase


class GetBooks(ObjectType):
    book_search = Field(List(Book), search=String())

    async def resolve_book_search(self, info, search):
        book_manage_use_case = BookManageUseCase()
        books_founded = await book_manage_use_case.process_book_data(search)
        return books_founded


class CreateBook(Mutation):
    class Arguments:
        id = String()
        resource = String()

    book = Field(SaveBookResponse)

    async def mutate(self, info, id, resource):
        book_manage_use_case = BookManageUseCase()
        book = Book(
            id=id,
            resource=resource
        )
        try:
            book_uploaded = await book_manage_use_case.save_book(book)
            return CreateBook(book=SaveBookResponse(
                id=book_uploaded.get("id"),
                message="Book successfully saved"
            ))
        except FileExistsError as error:
            return CreateBook(book=SaveBookResponse(
                id=id,
                message="Book already exists in database"
            ))


class DeleteBook(Mutation):
    class Arguments:
        book_id = ID(required=True)

    success = Boolean()
    message = String()

    async def mutate(self, info, book_id):
        delete_success = None
        try:
            book_manage_use_case = BookManageUseCase()
            delete_success = await book_manage_use_case.delete_book(book_id)
            return DeleteBook(success=bool(delete_success.deleted_count),
                              message="Delete book with id {} successfully".format(book_id))
        except FileNotFoundError:
            return DeleteBook(success=False,
                              message="Book not found")


class MyMutations(ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
