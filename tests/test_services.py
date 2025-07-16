import pandas as pd
import pytest

from src.services import investment_bank, preparing_list_transactions


@pytest.fixture()
def dict_transactions_for_investment():
    return [
        {
        "Дата операции": "2020-11",
        "Сумма операции": -11.5
    },
        {
        "Дата операции": "2020-11",
        "Сумма операции": -23.4
    },
        {
        "Дата операции": "2021-02",
        "Сумма операции": -15.47
    },
        {
        "Дата операции": "2021-02",
        "Сумма операции": -64.2
    },
        {
        "Дата операции": "2019-06",
        "Сумма операции": -72.12
    },
        {
        "Дата операции": "2019-08",
        "Сумма операции": -15.2
    },
        {
        "Дата операции": "2018-03",
        "Сумма операции": -84.1
    },
        {
        "Дата операции": "2018-04",
        "Сумма операции": -95.73
    }
]


@pytest.mark.parametrize(
    "month, dict_transactions_for_investment, limit, expected",
    [
        (
            "2020-11",
            dict_transactions_for_investment,
            50,
            65.1
        ),
        (
            "2025-11",
            dict_transactions_for_investment,
            50,
            0.0
        ),
        (
            "2020-11-12",
            dict_transactions_for_investment,
            100,
            "Неверно указана дата поиска"
        ),
        (
            "2020-11",
            dict_transactions_for_investment,
            150,
            ValueError
        )
    ],
    indirect=["dict_transactions_for_investment"]
)
def test_investment_bank_success(month, dict_transactions_for_investment, limit, expected):
    if expected is ValueError:
        with pytest.raises(expected):
            investment_bank(month, dict_transactions_for_investment, limit)
    else:
        assert investment_bank(month, dict_transactions_for_investment, limit) == expected


def test_preparing_list_transactions(my_dict_transactions):
    assert preparing_list_transactions(
        pd.DataFrame(my_dict_transactions)
    ) == [{'Дата операции': '2018-05-02', 'Сумма операции': -2.3}]