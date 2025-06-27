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
