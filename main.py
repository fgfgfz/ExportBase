from loguru import logger

from parsers import Parser
from settings import Settings


def main():
    Settings.logs.setup_logging()
    logger.info('Start program')
    parser = Parser()
    parser.get_companies()
    parser.get_companies_info()
    parser.print_bad_or_doubles()
    parser.load_data()
    logger.info('End program')


if __name__ == '__main__':
    main()
