import logging
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'reports.log')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def write_result_to_file(func: Callable) -> Any:
    """Декоратор для записи результатов в файл"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result: pd.DataFrame = func(*args, **kwargs)
        logger.info("Запись данных в файл")
        result.to_json(
            os.path.join(os.path.dirname(__file__), "..", "data", "reports_result", "spending.json"), force_ascii=False
        )

        return result

    return wrapper


def write_result_to_file_with_parameter(file_name: str = "result.json") -> Any:
    """Декоратор для записи результатов в файл, имя указывается параметром декоратора"""

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result: pd.DataFrame = func(*args, **kwargs)
            logger.info(f"Запись данных в файл с именем {file_name}")
            result.to_json(
                os.path.join(os.path.dirname(__file__), "..", "data", "reports_result", file_name), force_ascii=False
            )

            return result

        return wrapper

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | str:
    """Возвращает траты по заданной категории за последние 3 месяца"""

    logger.info("Вычисление начала и конца периода выборки")
    if date is None:
        stop_span = datetime.now()
    else:
        try:
            stop_span = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            logger.error("Передан неправильный формат даты")
            return "Неверный формат даты. Нужный формат - DD-MM-YYYY HH:MM:SS"

    logger.info("Подготовка конечного DataFrame")
    start_span = stop_span - relativedelta(months=3)

    df = transactions[
        (pd.to_datetime(transactions["Дата операции"], dayfirst=True) >= start_span)
        & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= stop_span)
    ]

    df = df[df["Категория"] == category].agg({"Сумма операции": "sum"})

    df["Категория"] = category

    return df
