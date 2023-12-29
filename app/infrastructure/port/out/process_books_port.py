from abc import ABC, abstractmethod


class FindBooksPort(ABC):

    @abstractmethod
    def find_book(self, query):
        pass
