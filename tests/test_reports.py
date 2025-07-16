import os
from unittest.mock import patch, mock_open

import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal

from src.reports import spending_by_category, write_result_to_file, write_result_to_file_with_parameter


def test_spending_by_category(my_dict_transactions):
    expected = pd.Series({"Сумма операции": 1.2, "Категория": "товар"})
    result = spending_by_category(pd.DataFrame(my_dict_transactions), "товар", '31-01-2022 15:00:00')
    assert_series_equal(result, expected)


def test_spending_by_category_no_data(my_dict_transactions):
    expected = pd.Series({"Сумма операции": 0.0, "Категория": "товар"})
    result = spending_by_category(pd.DataFrame(my_dict_transactions), "товар")
    assert_series_equal(result, expected)


def test_spending_by_category_error_format_date(my_dict_transactions):
    assert spending_by_category(
        pd.DataFrame(my_dict_transactions), "товар", '31-01.2022 15:00:00'
    ) == 'Неверный формат даты. Нужный формат - DD-MM-YYYY HH:MM:SS'


def test_decorator_write_result_to_file(my_dict_transactions):
    with patch('builtins.open', new_callable=mock_open) as mock_file:

        @write_result_to_file
        def example_function():
            return pd.DataFrame(my_dict_transactions)

        result = example_function()

        assert_frame_equal(result, pd.DataFrame(my_dict_transactions))

        mock_file.return_value.write.assert_called_once_with(
            f"{pd.DataFrame(my_dict_transactions).to_json(force_ascii=False)}"
        )


def test_decorator_write_result_to_file_with_parameter_empty(my_dict_transactions):

    with patch('builtins.open', new_callable=mock_open) as mock_file:
        @write_result_to_file_with_parameter()
        def example_function():
            return pd.DataFrame(my_dict_transactions)

        result = example_function()

        assert_frame_equal(result, pd.DataFrame(my_dict_transactions))

        mock_file.assert_called_once_with(
            os.path.join(
                "C:\\Users\\EasyGod\\PycharmProjects\\PythonProject\\transaction_analytics\\src",
                "..", "data", "reports_result", "result.json"), 'w', encoding='utf-8', errors='strict', newline=''
        )

        mock_file.return_value.write.assert_called_once_with(
            f"{pd.DataFrame(my_dict_transactions).to_json(force_ascii=False)}"
        )


def test_decorator_write_result_to_file_with_parameter(my_dict_transactions):

    with patch('builtins.open', new_callable=mock_open) as mock_file:
        @write_result_to_file_with_parameter("123.json")
        def example_function():
            return pd.DataFrame(my_dict_transactions)

        result = example_function()

        assert_frame_equal(result, pd.DataFrame(my_dict_transactions))

        mock_file.assert_called_once_with(
            os.path.join(
                "C:\\Users\\EasyGod\\PycharmProjects\\PythonProject\\transaction_analytics\\src",
                "..", "data", "reports_result", "123.json"), 'w', encoding='utf-8', errors='strict', newline=''
        )

        mock_file.return_value.write.assert_called_once_with(
            f"{pd.DataFrame(my_dict_transactions).to_json(force_ascii=False)}"
        )
