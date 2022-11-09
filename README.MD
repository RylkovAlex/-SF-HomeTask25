# Необходимые библиотеки

1. pip install pytest
2. pip install pytest-selenium
3. pip install python-environ

# Перед запуском

1. скачать драйвера для нужных браузеров
2. в папке test создать файл .env и в нём задать переменные:

   BASE_URL = 'https://petfriends.skillfactory.ru'

   USER_EMAIL = 'user@email.com'

   USER_PASSWORD = '*********'

# Запуск тестов

- pytest -v --driver [Browser] --driver-path [путь к драйверу]

Пример для Chrome:

- pytest -v --driver [Browser] --driver-path ./chromedriver.exe
