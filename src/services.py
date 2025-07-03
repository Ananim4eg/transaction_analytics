import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'services.log')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float | str:
    """Высчитывает сумму, которую мог бы накопить пользователь за указанный месяц, учитывая порог округления"""

    if limit not in [10, 50, 100]:
        logger.error("Неверно указан порог округления")
        raise ValueError("Неверно указан порог округления. Доступные варианты - 10, 50, 100")

    result_amount = 0

    try:
        target_month = datetime.strptime(month, '%Y-%m').month
        target_year = datetime.strptime(month, '%Y-%m').year
    except ValueError:
        logger.error("Неверно указана дата поиска")
        return "Неверно указана дата поиска"

    logger.info("Начало подсчета суммы накоплений")
    for item in transactions:
        date_transactions = datetime.strptime(item["Дата операции"], '%Y-%m-%d')
        if date_transactions.month == target_month and date_transactions.year == target_year:
            result_amount += limit - (abs(item["Сумма операции"]) % limit)
    logger.info("Конец подсчета суммы накоплений")

    return round(result_amount, 2)


def preparing_list_transactions(my_list_transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Обрабатывает dataframe с информацией о транзакциях, возвращает список словарей с датой и суммой транзакций"""

    result = []

    logger.info("Подготовка DataFrame")
    df = my_list_transactions[my_list_transactions["Статус"] == "OK"].loc[:, ['Сумма операции', 'Дата операции']]
    df = df[df['Сумма операции'] < 0].reset_index(drop=True)

    logger.info("Начало формирования списка из дат и сумм транзакций")
    for index in range(len(df)):
        date = datetime.strptime(df.loc[:, 'Дата операции'][index], "%d.%m.%Y %H:%M:%S")
        date_formated = datetime.strftime(date, '%Y-%m-%d')

        result.append(
            {
                "Дата операции": date_formated,
                "Сумма операции": float(df.loc[:, 'Сумма операции'][index])
            }
        )
    logger.info("Конец формирования списка")

    return result
