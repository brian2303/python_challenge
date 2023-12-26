from abc import ABC, abstractmethod


class ProcessBooksPort(ABC):

    @abstractmethod
    def find_book(self, query):
        pass
