from graphene import ObjectType, Field, List, String

from app.domain.model.book_model import Book
from app.domain.usecase.book_manage_use_case import BookManageUseCase


class BookRouter(ObjectType):
    book_search = Field(List(Book), search=String())

    async def resolve_book_search(self, info, search):
        book_manage_use_case = BookManageUseCase()
        books_founded = await book_manage_use_case.process_book_data(search)
        return books_founded
