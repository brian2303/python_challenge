import logging


class AppUtils:

    @staticmethod
    def log_conf():
        return logging.basicConfig(level=logging.WARNING,
                                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
