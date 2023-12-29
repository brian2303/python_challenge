from abc import ABC, abstractmethod


class CreateUserPort(ABC):

    @abstractmethod
    def create_user(self, username, password):
        pass

    @abstractmethod
    def find_by_username(self, username):
        pass

    @abstractmethod
    def check_user(self, username, password):
        pass
