# Парсер данных из XML и загрузка их в БД

### Используемые инструменты
* Python 3.13.2 `https://www.python.org/downloads/`
* PostgreSQL 16 `https://www.enterprisedb.com/downloads/postgres-postgresql-downloads`

### Подготовка и запуск
1. Создать папку для проекта **(последующие python команды использовать в консоли в папке проекта)**
2. Скачать проект из репозитория в папку проекта (`<> Code -> Download ZIP` и распаковать или, например в PyCharm, `Get from VCS` -> `https://github.com/fgfgfz/ExportBase.git`)
3. Создать виртуальное окружение `python -m venv [название]` и запустить его `[название]/Scripts/activate` если не запустилось автоматически
4. Загрузить библиотеки `pip install -r requirements.txt`
5. Создать в postgres базу данных или использовать существующую
6. Заполнить файл `.env` информацией для подключения к базе данных:
   ```
   LOGIN=[login]
   PASSWORD=[password]
   HOST=[host]
   PORT=[port]
   DATABASE=[database]
   SCHEMA=[schema]
   ```
7. Запустить файл `main.py` командой `python main.py`

### Результатом работы будет:
* Валидные данные будут загружены в БД
* Невалидные данные будут выведены в консоль
* Также создастся файл с логами `logs.log`