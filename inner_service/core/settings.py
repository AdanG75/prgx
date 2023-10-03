import os
from pathlib import Path

from dotenv import load_dotenv


class Settings(object):
    __POSTGRES_USER: str
    __POSTGRES_PASSWORD: str
    __POSTGRES_MAIN_DB: str
    __POSTGRES_TEST_DB: str
    __POSTGRES_SERVER: str
    __POSTGRES_PORT: int
    __DATABASE_URL: str

    def __init__(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        self.__POSTGRES_USER = os.environ.get("POSTGRES_USER")
        self.__POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
        self.__POSTGRES_TEST_DB = os.environ.get("POSTGRES_TEST_DB")
        self.__POSTGRES_MAIN_DB = os.environ.get("POSTGRES_MAIN_DB")
        self.__POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
        self.__POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT"))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)

        return cls.instance

    def get_database_url(self, test_db: bool = False):
        postgres_db = self.__POSTGRES_TEST_DB if test_db else self.__POSTGRES_MAIN_DB

        self.__DATABASE_URL = f"postgresql://" \
                              f"{self.__POSTGRES_USER}:{self.__POSTGRES_PASSWORD}@" \
                              f"{self.__POSTGRES_SERVER}:{self.__POSTGRES_PORT}/" \
                              f"{postgres_db}"

        return self.__DATABASE_URL


def charge_settings() -> Settings:
    setting = Settings()

    return setting


settings = Settings()