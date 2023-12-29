from abc import ABC, abstractmethod


class CreateBooksPort(ABC):

    @abstractmethod
    def insert_data_from_external_requests(self, raw_data_book):
        pass
