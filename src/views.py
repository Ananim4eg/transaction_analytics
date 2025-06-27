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
