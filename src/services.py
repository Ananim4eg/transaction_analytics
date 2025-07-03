from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float | str:
    """Высчитывает сумму, которую мог бы накопить пользователь за указанный месяц, учитывая порог округления"""

    if limit not in [10, 50 , 100]:
        raise ValueError("Неверно указан порог округления. Доступные варианты - 10, 50, 100")

    result_amount = 0

    try:
        target_month = datetime.strptime(month, '%Y-%m').month
        target_year = datetime.strptime(month, '%Y-%m').year
    except ValueError:
        return "Неверно указана дата поиска"

    for item in transactions:
        date_transactions = datetime.strptime(item["Дата операции"], '%Y-%m-%d')
        if date_transactions.month == target_month and date_transactions.year == target_year:
            result_amount += limit - (abs(item["Сумма операции"]) % limit)

    return round(result_amount, 2)


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
