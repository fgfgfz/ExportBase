from os import getenv

from dotenv import load_dotenv
from loguru import logger


load_dotenv()


class General:
    file_name: str = 'companies.xml'


class DatabaseConfig:
    LOGIN = getenv('LOGIN')
    PASSWORD = getenv('PASSWORD')
    HOST = getenv('HOST')
    PORT = getenv('PORT')
    DATABASE = getenv('DATABASE')
    SCHEMA = getenv('SCHEMA')
    connection_string = f'postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


class LogsConfig:
    @classmethod
    def setup_logging(cls):
        logger.remove()
        logger.add(
            'logs.log',
            level='DEBUG',
            format='<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> | '
                   '<level>{level: <8}</level> | '
                   '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
                   '<level>{message}</level>'
        )


class Settings:
    general: General = General()
    db: DatabaseConfig = DatabaseConfig()
    logs: LogsConfig = LogsConfig()
