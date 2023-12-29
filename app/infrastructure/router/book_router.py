from graphene import ObjectType, Field, List, String

from app.infrastructure.router.models.book_model import Book
from app.domain.usecase.find_book_use_case import FindBookUseCase
from app.infrastructure.router.delete_book_router import DeleteBook
from app.infrastructure.router.create_book_router import CreateBook


class GetBooks(ObjectType):
    book_search = Field(List(Book), search=String())

    async def resolve_book_search(self, info, search):
        find_book_use_case = FindBookUseCase()
        books_founded = await find_book_use_case.process_book_data(search)
        return books_founded


class MyMutations(ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
