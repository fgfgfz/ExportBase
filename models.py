from sqlalchemy import (
    MetaData,
    String,
    Date
)
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column
)

from settings import Settings


Base = declarative_base(metadata=MetaData(schema=Settings.db.SCHEMA))


class Company(Base):
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(primary_key=True)
    ogrn: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    inn: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(500))
    date: Mapped[Date] = mapped_column(Date, nullable=False)
