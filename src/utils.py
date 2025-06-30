import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'utils.log')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_xlsx_file(path_file: str) -> pd.DataFrame | str:
    """Считывает xlsx файл и возвращает список словарей с транзакциями"""

    try:
        logger.info("Чтение файла .xlsx")
        excel_data = pd.read_excel(path_file)

        return excel_data

    except FileNotFoundError:
        logger.error("Ошибка чтения файла. Файл не найден")
        return "Файл не найден"


def read_json_file(path_file: str) -> dict | str:
    """Считывает json-файл и возвращает словарь"""

    try:
        logger.info("Чтение json-файла с настройками")
        with open(path_file, encoding='utf-8') as settings:
            result = json.load(settings)

    except FileNotFoundError:
        logger.error("Ошибка чтения файла")
        return "Ошибка чтения файла."

    return result


def get_top_transactions(list_transactions: pd.DataFrame) -> list[dict]:
    """Получение топ-5 операций по их сумме"""
    top_transactions = []
    length = 5

    if list_transactions.empty:
        return []

    df = list_transactions[list_transactions["Статус"] == "OK"]
    df = df.sort_values(by='Сумма операции', key=abs, ascending=False).head()

    if len(df) < 5:
        length = len(df)

    logger.info("Начало формирования списка из 5-и самых частых категорий транзакций")
    for _ in range(length):
        date_format = df.loc[:, 'Дата операции'].iloc[_].split()[0]

        if type(df.loc[:, 'Категория'].iloc[_]) is float:
            category_transaction = "Без категории"
        else:
            category_transaction = df.loc[:, 'Категория'].iloc[_]
        top_transactions.append(
            {
                "date": date_format,
                "amount": abs(float(df.loc[:, 'Сумма операции'].iloc[_])),
                "category": category_transaction,
                "description": df.loc[:, 'Описание'].iloc[_]
            }
        )
    logger.info("Конец формирования списка")

    return top_transactions


def get_card_expenses(list_transactions: pd.DataFrame) -> list[dict]:
    """Получение расходов по каждой карте"""

    card_info = []

    if list_transactions.empty:
        return []

    df = list_transactions.groupby('Номер карты').agg({'Сумма операции': 'sum'})
    line_card_expenses = df.iterrows()

    logger.info("Начало формирования списка расходов по каждой карте")
    for i in range(len(df)):
        next_line = next(line_card_expenses)
        card_info.append(
            {
                "last_digits": next_line[0][1:],
                "total_spent": abs(float(df.loc[next_line[0]].iloc[0])),
                "cashback": round(float(abs(df.loc[next_line[0]].iloc[0])) / 100, 2)
            }
        )
    logger.info("Конец формирования списка")
    return card_info


def get_currency_rates(settings: dict) -> list[dict] | str:
    """Получает курсы валют, указанных в файле user_settings.json"""
    list_currency_rates = []

    currency = settings["user_currencies"]

    load_dotenv()

    logger.info("Начало формирования списка курса валют")
    for cur in currency:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur}&amount=1"
        headers = {'apikey': os.getenv("API_KEY_FOR_APILAYER")}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            list_currency_rates.append(
                {
                    "currency": cur,
                    "rate": round(response.json()["result"], 2)
                }
            )
        else:
            logger.error("Ошибка получения курса валюты")
            return "Произошла ошибка при получении курса валюты"
    logger.info("Конец формирования списка")

    return list_currency_rates


def get_stock_prices(settings: dict) -> list[dict] | str:
    """Получает цены акций, указанных в файле user_settings.json"""
    list_stock_prices = []

    stocks = settings["user_stocks"]

    load_dotenv()
    date_today = datetime.today().strftime('%Y-%m-%d')

    logger.info("Начало формирования списка стоимостей акций")
    for stock in stocks:
        url = (f'https://financialmodelingprep.com/stable/historical-price-eod/light?symbol={stock}'
               f'&from={date_today}'
               f'&apikey={os.getenv("API_KEY_FOR_FMP")}')

        response = requests.get(url)

        if response.status_code == 200:
            list_stock_prices.append(
                {
                    "stock": f"{stock}",
                    "price": response.json()[0]["price"]
                }
            )
        else:
            logger.error("Ошибка получения информации о стоимости акции")
            return "Ошибка подключения"
    logger.info("Конец формирования списка")

    return list_stock_prices
