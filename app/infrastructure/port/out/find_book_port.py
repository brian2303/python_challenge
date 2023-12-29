from abc import ABC, abstractmethod


class FindBookPort(ABC):

    @abstractmethod
    def find_book(self, query):
        pass

    @abstractmethod
    def search_book_google_api_by_id(self, book_id):
        pass

    @abstractmethod
    def search_book_open_library_api_by_id(self, book_id):
        pass

    @abstractmethod
    def get_all_external_data(self, param):
        pass
