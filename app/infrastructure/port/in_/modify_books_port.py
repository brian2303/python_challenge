from abc import ABC, abstractmethod


class ModifyBooksPort(ABC):

    @abstractmethod
    def get_all_external_data(self, param):
        pass

    @abstractmethod
    def delete_book_by_id(self, book_id):
        pass
