from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import Error as PostgresError
from loguru import logger

from settings import Settings
from models import (
    Base,
    Company
)


class Engine:
    def __init__(self):
        try:
            self.engine = create_engine(Settings.db.connection_string)
            self.Session = sessionmaker(bind=self.engine)
        except (PostgresError, SQLAlchemyError) as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    def create_table(self):
        logger.info('Creating table')
        try:
            Base.metadata.create_all(self.engine)
        except (PostgresError, SQLAlchemyError) as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    def insert_companies(self, companies: list[dict[str, str | date]]):
        logger.info('Inserting data')
        with self.Session() as session:
            try:
                session.add_all([Company(**company) for company in companies])
                session.commit()
            except (PostgresError, SQLAlchemyError) as exception:
                logger.exception(f'{exception.__class__.__name__}: {exception}')
