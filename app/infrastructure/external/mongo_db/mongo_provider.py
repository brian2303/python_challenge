import os
import motor.motor_asyncio
import logging
from dotenv import load_dotenv
from app.app_utils import AppUtils
from bson.regex import Regex


class MongoProvider:
    AppUtils.log_conf()
    load_dotenv()

    def __init__(self, collection):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.str_connection = os.getenv("STR_CONNECT")
        self.collection = collection

    def __connect_conf(self):
        str_connection = self.str_connection.format(
            username=self.user,
            password=self.password
        )

        client = motor.motor_asyncio.AsyncIOMotorClient(str_connection)
        db = client[self.db_name]
        logging.info("Get connection")
        return db[self.collection]

    async def find_one(self, query):
        conn = self.__connect_conf()
        query_built = self.__build_query(query)
        data = await conn.find_one(query_built)
        logging.info("Get data successfully")
        return data

    async def insert(self, data):
        conn = self.__connect_conf()
        data = await conn.insert_many(data)
        logging.info("Save data successfully")
        return data

    async def delete(self, query):
        conn = self.__connect_conf()
        data = conn.find_one(query)
        if data is not None:
            await conn.delete_one(query)
            logging.info("delete data")
        logging.info("File not found in_ db")
        raise FileNotFoundError

    @classmethod
    def __build_query(cls, query):
        full_query = Regex(f".*{query}.*", 'i')
        return {
            "$or": [
                {"id": full_query},
                {"title": full_query},
                {"subtitle": full_query},
                {"authors": full_query},
                {"categories": full_query},
                {"published_date": full_query},
                {"editor": full_query},
                {"description": full_query},
                {"image.some_key": full_query}
            ]
        }
