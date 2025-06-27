import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
import pandas as pd


def main_page(date):
    ...


def read_xlsx_file(path_file: str) -> pd.DataFrame | str:
    """Считывает xlsx файл и возвращает список словарей с транзакциями"""

    try:
        excel_data = pd.read_excel(path_file)

        return excel_data

    except FileNotFoundError:
        return "Файл не найден"

def get_top_transactions(list_transactions: pd.DataFrame) -> list[dict]:
    """Получение топ-5 операций по их сумме"""
    top_transactions = []

    df = list_transactions.sort_values(by='Сумма операции').head()

    for _ in range(5):
        date_format = df.loc[:,'Дата операции'].iloc[_].split()[0]

        if type(df.loc[:,'Категория'].iloc[_]) is float:
            category_transaction = "Без категории"
        else:
            category_transaction = df.loc[:,'Категория'].iloc[_]
        top_transactions.append(
            {
                "date": date_format,
                "amount": abs(float(df.loc[:,'Сумма операции'].iloc[_])),
                "category": category_transaction,
                "description": df.loc[:,'Описание'].iloc[_]
            }
        )

    return top_transactions


def get_card_expenses(list_transactions: pd.DataFrame) -> list[dict]:
    """Получение расходов по каждой карте"""

    card_info =[]

    df = list_transactions.groupby('Номер карты').agg({'Сумма операции': 'sum'})
    line_card_expenses = df.iterrows()

    for i in range(len(df)):
        next_line = next(line_card_expenses)
        card_info.append(
            {
                "last_digits": next_line[0][1:],
                "total_spent": abs(float(df.loc[next_line[0]].iloc[0])),
                "cashback": round(float(abs(df.loc[next_line[0]].iloc[0])) / 100, 2)
            }
        )
    return card_info


def get_currency_rates() -> list[dict] | str:
    """Получает курсы валют, указанных в файле user_settings.json"""
    list_currency_rates = []
    path_to_file_with_settings = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')

    with open(path_to_file_with_settings, encoding='utf-8') as settings:
        currency = json.load(settings)["user_currencies"]

    load_dotenv()

    for cur in currency:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur}&amount=1"
        headers = {'apikey':os.getenv("API_KEY_FOR_APILAYER")}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            list_currency_rates.append(
                {
                    "currency": cur,
                    "rate": round(response.json()["result"], 2)
                }
            )
        else:
            return "Произошла ошибка при получении курса валюты"

    return list_currency_rates


def get_stock_prices() -> list[dict] | str:
    """Получает цены акций, указанных в файле user_settings.json"""
    list_stock_prices =[]
    path_to_file_with_settings = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')

    with open(path_to_file_with_settings, encoding='utf-8') as settings:
        stocks = json.load(settings)["user_stocks"]

    load_dotenv()
    date_today = datetime.today().strftime('%Y-%m-%d')

    for stock in stocks:
        url = (f'https://financialmodelingprep.com/stable/historical-price-eod/light?symbol={stock}'
               f'&from={date_today}'
               f'&apikey={os.getenv("API_KEY_FOR_FMP")}')

        response = requests.get(url)

        if response.status_code == 200:
            print(*response.json())
            list_stock_prices.append(
                {
                    "stock": f"{stock}",
                    "price": response.json()[0]["price"]
                }
            )
        else:
            return "Ошибка подключения"

    return list_stock_prices
