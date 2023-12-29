from abc import ABC, abstractmethod


class DeleteBookPort(ABC):

    @abstractmethod
    def delete_book_by_id(self, book_id):
        pass
