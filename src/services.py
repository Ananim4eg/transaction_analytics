from datetime import datetime
from typing import List, Dict, Any

import pandas as pd

from src.utils import read_xlsx_file


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    ...


def preparing_list_transactions(my_list_transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Обрабатывает dataframe с информацией о транзакциях, возвращает список словарей с датой и суммой транзакций"""

    result = []

    df = my_list_transactions[my_list_transactions["Статус"] == "OK"].loc[:, ['Сумма операции', 'Дата операции']]
    df = df[df['Сумма операции'] < 0].reset_index(drop=True)

    for index in range(len(df)):
        date = datetime.strptime(df.loc[:, 'Дата операции'][index], "%d.%m.%Y %H:%M:%S")
        date_formated = datetime.strftime(date, '%Y-%m-%d')

        result.append(
            {
                "Дата операции": date_formated,
                "Сумма операции": float(df.loc[:, 'Сумма операции'][index])
            }
        )

    return result
