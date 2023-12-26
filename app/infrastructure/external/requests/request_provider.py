import requests
import logging
from app.app_utils import AppUtils


class RequestsProvider:
    AppUtils.log_conf()

    def __init__(self, url):
        self.url = url

    def get_request(self, params):
        try:
            response = requests.get(self.url, params=params, timeout=10)
            if response.status_code is 200:
                return response.json()
        except requests.Timeout:
            logging.error("Close connection by timeout")
        except requests.RequestException:
            logging.error("Request error")
