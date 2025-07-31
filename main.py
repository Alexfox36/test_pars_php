import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

BASE_URL = "http://185.244.219.162/phpmyadmin"
LOGIN_URL = f"{BASE_URL}/index.php"
DB_URL = f"{BASE_URL}/index.php?route=/database/structure&db=testDB"
TABLE_URL_TEMPLATE = f"{BASE_URL}/index.php?route=/sql&db=testDB&table=users&pos=0"
USERNAME = "test"
PASSWORD = "JHFBdsyf2eg8*"
session = requests.Session()

def log_debug(filename: str, html: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Сохранён HTML в файл: {filename}")

resp = session.get(LOGIN_URL)
soup = BeautifulSoup(resp.text, "html.parser")
token_input = soup.find("input", {"name": "token"})

if not token_input:
    print("Не найден токен перед логином.")
    log_debug("debug_token_before_login.html", resp.text)
    exit()
token = token_input["value"]
print(f"Токен перед логином: {token}")

login_payload = {
    "pma_username": USERNAME,
    "pma_password": PASSWORD,
    "server": 1,
    "target": "index.php",
    "lang": "ru",
    "token": token
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}
resp = session.post(LOGIN_URL, data=login_payload, headers=headers)
if "phpMyAdmin" not in resp.text:
    print("Авторизация не произошла.")
    log_debug("debug_auth_fail.html", resp.text)
    exit()
print("Авторизация прошла успешно")

resp = session.get(LOGIN_URL)
soup = BeautifulSoup(resp.text, "html.parser")
new_token_input = soup.find("input", {"name": "token"})
if new_token_input:
    token = new_token_input["value"]
    print(f"Получен новый рабочий токен: {token}")
else:
    print("Токен после логина не получен")
    log_debug("debug_token_after_login.html", resp.text)
    exit()

headers_with_referer = {
    "User-Agent": "Mozilla/5.0",
    "Referer": LOGIN_URL
}
session.get(DB_URL + f"&token={token}", headers=headers_with_referer)
table_url = TABLE_URL_TEMPLATE + f"&token={token}"
resp = session.get(table_url, headers=headers_with_referer)
print(f"Статус код получения таблицы: {resp.status_code}")
log_debug("debug.html", resp.text)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", {"class": "table_results"})

if not table:
    print("Таблица users не найдена.")
    exit()
rows = table.find_all("tr")[1:]
data = []
for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        id_val = cols[-2].get_text(strip=True)
        name_val = cols[-1].get_text(strip=True)
        data.append([id_val, name_val])
print("\nТаблица users:\n")
print(tabulate(data, headers=["id", "name"], tablefmt="grid"))