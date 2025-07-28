import requests
from bs4 import BeautifulSoup

# URL phpMyAdmin
url = 'http://185.244.219.162/phpmyadmin'

# Данные для авторизации
payload = {
    'pma_username': 'test',
    'pma_password': 'JHFBdsyf2eg8*',
    'server': '1',  # номер сервера, обычно 1
    'target': 'db_structure.php',
    'db': 'testDB'
}

# Создание сессии
session = requests.Session()

# Авторизация
response = session.post(url, data=payload)

# Проверка успешности авторизаци
if response.status_code == 200 and 'phpMyAdmin' in response.text:
    print("Авторизация успешна.")
else:
    print("Ошибка авторизации.")
    exit()

# Переход к базе данных testDB
db_url = f'{url}/index.php?route=/table/structure&db=testDB'
db_response = session.get(db_url)

# Проверка успешности перехода
if db_response.status_code != 200:
    print("Ошибка перехода к базе данных.")
    exit()

# Извлечение содержимого таблицы users
soup = BeautifulSoup(db_response.text, 'html.parser')
table = soup.find('table', {'id': 'table_users'})  # Найти таблицу users по ID (может быть другим)

if not table:
    print("Таблица users не найдена.")
    exit()

# Получение строк из таблицы
rows = table.find_all('tr')

# Вывод данных в читаемом виде
for row in rows:
    cols = row.find_all('td')
    data = [col.text.strip() for col in cols]
    print(data)
