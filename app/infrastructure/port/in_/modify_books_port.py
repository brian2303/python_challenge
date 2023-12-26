from abc import ABC, abstractmethod


class ModifyBooksPort(ABC):

    @abstractmethod
    def insert_book(self, book):
        pass

    @abstractmethod
    def get_external_data(self, param):
        pass
