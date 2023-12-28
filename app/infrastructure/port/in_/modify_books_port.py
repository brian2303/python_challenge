from abc import ABC, abstractmethod


class ModifyBooksPort(ABC):

    @abstractmethod
    def insert_book(self, book):
        pass

    @abstractmethod
    def get_all_external_data(self, param):
        pass

    @abstractmethod
    def insert_data_from_external_requests(self, raw_data_book):
        pass
