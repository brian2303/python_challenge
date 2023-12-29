from graphene import Field, String, Mutation
from app.infrastructure.router.models.save_book_response import SaveBookResponse
from app.domain.usecase.create_book_use_case import CreateBookUseCase
from app.infrastructure.router.models.book_model import Book


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
