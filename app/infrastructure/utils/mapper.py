from app.domain.model.book_dto import BookDTO


class MapperUtils:

    FIRST_ID = 0

    @classmethod
    def map_to_google_book_model(cls, request_response):
        return BookDTO(
            id=request_response.get("id"),
            title=request_response.get("volumeInfo").get("title"),
            subtitle=request_response.get("volumeInfo").get("subtitle", ""),
            authors=request_response.get("volumeInfo").get("authors", []),
            categories=request_response.get("volumeInfo").get("categories", []),
            published_date=request_response.get("volumeInfo").get("publishedDate", ""),
            editor=request_response.get("volumeInfo").get("publisher", ""),
            description=request_response.get("volumeInfo").get("description", ""),
            image=request_response.get("volumeInfo").get("imageLinks", {}).get("large", "")
        ).model_dump()

    @classmethod
    def map_to_open_library_book_model(cls, request_response):
        return BookDTO(
            id=MapperUtils.__validate_list(request_response.get("isbn", [])),
            title=request_response.get("title", ""),
            subtitle="",
            authors=request_response.get("author_name", []),
            categories=request_response.get("subject_key", []),
            published_date=MapperUtils.__validate_list(request_response.get("publish_date", [])),
            editor="",
            description="",
            image=""
        ).model_dump()

    @classmethod
    def __validate_list(cls, list_str):
        return list_str[MapperUtils.FIRST_ID] if len(list_str) > 0 else ""
