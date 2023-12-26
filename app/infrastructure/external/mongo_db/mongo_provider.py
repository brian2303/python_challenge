import os
import motor.motor_asyncio
import logging
from app.app_utils import AppUtils


class MongoProvider:
    AppUtils.log_conf()

    def __init__(self, collection):
        self.db_name = os.getenv("DB_NAME")
        self.user = os.getenv("USERNAME")
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
        data = await conn.find_one(query)
        logging.info("Get data successfully")
        return data

    async def insert(self, data):
        conn = self.__connect_conf()
        data = await conn.insert_one(data)
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
