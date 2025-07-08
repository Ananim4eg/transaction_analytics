import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def write_result_to_file(func: Callable) -> Any:
    """Декоратор для записи результатов в файл"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result: pd.DataFrame = func(*args, **kwargs)
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
            result.to_json(
                os.path.join(os.path.dirname(__file__), "..", "data", "reports_result", file_name), force_ascii=False
            )

            return result

        return wrapper

    return decorator


@write_result_to_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | str:
    """Возвращает траты по заданной категории за последние 3 месяца"""

    if date is None:
        stop_span = datetime.now()
    else:
        try:
            stop_span = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            return "Неверный формат даты. Нужный формат - DD-MM-YYYY HH:MM:SS"

    start_span = stop_span - relativedelta(months=3)

    df = transactions[
        (pd.to_datetime(transactions["Дата операции"], dayfirst=True) >= start_span)
        & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= stop_span)
    ]

    df = df[df["Категория"] == category].agg({"Сумма операции": "sum"})

    df["Категория"] = category

    return df
