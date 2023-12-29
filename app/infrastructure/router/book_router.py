from graphene import ObjectType, Field, List, String, Mutation, ID, Boolean

from app.infrastructure.router.models.book_model import Book
from app.infrastructure.router.models.save_book_response import SaveBookResponse
from app.domain.usecase.book_manage_use_case import BookManageUseCase
from app.domain.usecase.create_book_use_case import CreateBookUseCase
from app.infrastructure.router.delete_book_router import DeleteBook


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
        create_book_use_case = CreateBookUseCase()
        book = Book(
            id=id,
            resource=resource
        )
        try:
            book_uploaded = await create_book_use_case.save_book(book)
            return CreateBook(book=SaveBookResponse(
                id=book_uploaded.get("id"),
                message="Book successfully saved",
                title=book_uploaded.get("title"),
                subtitle=book_uploaded.get("subtitle")
            ))
        except FileExistsError as error:
            return CreateBook(book=SaveBookResponse(
                id=id,
                message="Book already exists in database",
                title="",
                subtitle=""
            ))





class MyMutations(ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
