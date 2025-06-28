import json
import os
from datetime import datetime

from src.utils import get_card_expenses, read_xlsx_file, get_top_transactions, get_currency_rates, get_stock_prices

path_to_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.xlsx')


def main_page(date: str) -> str:
    """Формирует результирующий список"""
    time_now = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()

    if 6 <= time_now.hour < 10:
        greeting = "Доброе утро"
    elif 10 <= time_now.hour < 17:
        greeting = "Добрый день"
    elif 17 <= time_now.hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    result_list = {
            "greeting": greeting,
            "cards": get_card_expenses(read_xlsx_file(path_to_file)),
            "top_transactions": get_top_transactions(read_xlsx_file(path_to_file)),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices()
        }

    return json.dumps(result_list, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    ...
    # print(main_page('2025-06-27 10:24:00'))