import os
from unittest.mock import patch, Mock

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from src.utils import read_xlsx_file, get_top_transactions, get_card_expenses, read_json_file, get_currency_rates, \
    get_stock_prices


def test_read_xlsx_file_success(my_dict):
    test_data = pd.DataFrame(my_dict)

    with patch('pandas.read_excel') as mocked_open:
        mocked_open.return_value = test_data
        result = read_xlsx_file('test.xlsx')

    assert_frame_equal(result, test_data)

    mocked_open.assert_called_once_with('test.xlsx')


def test_read_xlsx_file_error():
    assert read_xlsx_file('123') == 'Файл не найден'


def test_read_json_file_success():
    path_to_file = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')

    assert read_json_file(path_to_file) == {
        'user_currencies': ['USD', 'EUR'],
        'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    }


def test_read_json_file_error():
    path_to_file = os.path.join(os.path.dirname(__file__), 'user_settings.json')

    assert read_json_file(path_to_file) == "Ошибка чтения файла."


def test_get_top_transactions_success(my_dict_transactions):
    test_data = pd.DataFrame(my_dict_transactions)

    assert get_top_transactions(test_data) == [
        {'amount': 4.3, 'category': 'товар', 'date': '04.11.2019', 'description': 'хайт'},
        {'amount': 2.3, 'category': 'Без категории', 'date': '02.05.2018', 'description': 'мидл'},
        {'amount': 1.2, 'category': 'товар', 'date': '31.12.2021', 'description': 'топ'}
    ]


def test_get_top_transactions_empty_dataframe():
    test_data = pd.DataFrame([])

    assert get_top_transactions(test_data) == []


def test_get_card_expenses_success(my_dict_transactions):
    test_data = pd.DataFrame(my_dict_transactions)

    assert get_card_expenses(test_data) == [
        {'cashback': 0.02, 'last_digits': '4556', 'total_spent': 2.2},
        {'cashback': 0.02, 'last_digits': '7197', 'total_spent': 2.0}
    ]


def test_get_card_expenses_empty_dataframe():
    test_data = pd.DataFrame([])

    assert get_card_expenses(test_data) == []


@patch('requests.get')
def test_get_currency_rates_success(mock_get, my_dick_settings):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
         'success': True,
         'query': {'from': 'EUR', 'to': 'RUB', 'amount': 1},
         'info': {'timestamp': 1751279956, 'rate': 92.06522},
         'date': '2025-06-30',
         'result': 92.06522
        }

    mock_get.return_value = mock_response

    assert get_currency_rates(my_dick_settings) == [{'currency': 'EUR', 'rate': 92.07}]
    mock_get.assert_called_once()


@patch('requests.get')
def test_get_currency_rates_code_not_200(mock_get, my_dick_settings):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = None

    mock_get.return_value = mock_response

    assert get_currency_rates(my_dick_settings) == "Произошла ошибка при получении курса валюты"
    mock_get.assert_called_once()


@patch('requests.get')
def test_get_stock_prices_success(mock_get, my_dick_settings):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
      {
        "symbol": "AMZN",
        "date": "2025-06-26",
        "price": 214.0378,
        "volume": 9261299
      }
    ]

    mock_get.return_value = mock_response

    assert get_stock_prices(my_dick_settings) == [{'price': 214.0378, 'stock': 'AMZN'}]
    mock_get.assert_called_once()


@patch('requests.get')
def test_get_stock_prices_code_not_200(mock_get, my_dick_settings):

    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = None

    mock_get.return_value = mock_response

    assert get_stock_prices(my_dick_settings) == "Ошибка подключения"
    mock_get.assert_called_once()
