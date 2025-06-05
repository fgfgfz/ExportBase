import xml.etree.ElementTree as ET
from _elementtree import Element
from typing import Literal
from datetime import (
    date,
    datetime as dt
)

from loguru import logger

from settings import Settings
from database import Engine


class XmlParser:
    @staticmethod
    def get_companies() -> list[Element] | None:
        try:
            tree = ET.parse(Settings.general.file_name)
            root = tree.getroot()
            companies = root.findall('КОМПАНИЯ')
            return companies
        except AttributeError as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    @staticmethod
    def get_info_by_tag_name(
            company: Element,
            type_: Literal['ОГРН', 'ИНН', 'НазваниеКомпании']
    ) -> str | None:
        logger.info(f'Getting {type_}')
        try:
            info = company.find(type_).text
            return info
        except AttributeError as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    @staticmethod
    def get_phone_number(company: Element) -> str | None:
        logger.info(f'Getting phone number')
        try:
            phone_number = company.findall('Телефон')
            phone_number = [number.text for number in phone_number]
            phone_number = ', '.join(phone_number)
            return phone_number if phone_number else None
        except (AttributeError, TypeError) as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    @staticmethod
    def get_date(company: Element) -> date | None:
        logger.info(f'Getting date')
        try:
            date_ = company.find('ДатаОбн').text
            date_ = dt.strptime(date_, '%Y-%m-%d').date()
            return date_
        except AttributeError as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    @staticmethod
    def check_info(
            ogrn: str,
            inn: str,
            date_: date
    ) -> bool:
        logger.info(f'Checking company info')
        if (
                not date_
                or not ogrn
                or not inn
                or not ogrn.isdigit()
                or len(ogrn) != 13
                or not inn.isdigit()
                or len(inn) != 10
        ):
            return False
        return True



class Parser:
    def __init__(self):
        self.ogrn: list[str] = []
        self.good_companies: list[dict[str, str | date]] = []
        self.bad_or_doubles: list[dict[str, str | date | None]] = []
        self.companies: list[Element] = []

    def get_companies(self):
        logger.info('Getting companies')
        try:
            self.companies = XmlParser.get_companies()
            self.companies.sort(key=lambda x:(x[0].text, -dt.strptime(x[-1].text, '%Y-%m-%d').timestamp()))
        except AttributeError as exception:
            logger.exception(f'{exception.__class__.__name__}: {exception}')

    def get_companies_info(self):
        logger.info('Getting companies info')
        for company in self.companies:
            logger.info(company[2].text)
            ogrn = XmlParser.get_info_by_tag_name(company, 'ОГРН')
            inn = XmlParser.get_info_by_tag_name(company, 'ИНН')
            name = XmlParser.get_info_by_tag_name(company, 'НазваниеКомпании')
            phone_number = XmlParser.get_phone_number(company)
            date_ = XmlParser.get_date(company)
            good = XmlParser.check_info(ogrn, inn, date_)
            info = {
                'ogrn': ogrn,
                'inn': inn,
                'name': name,
                'phone_number': phone_number,
                'date': date_,
            }

            if not good:
                self.bad_or_doubles.append(info)

            if good and ogrn in self.ogrn:
                self.bad_or_doubles.append(info)

            if good and ogrn not in self.ogrn:
                self.good_companies.append(info)
                self.ogrn.append(ogrn)

    def print_bad_or_doubles(self):
        logger.info('Printing bad or doubles')
        for company in self.bad_or_doubles:
            for key, value in company.items():
                print(f'{key}: {value}')
            print()

    def load_data(self):
        logger.info('Loading data')
        engine = Engine()
        engine.create_table()
        engine.insert_companies(self.good_companies)
