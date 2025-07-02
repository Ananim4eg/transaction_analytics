from cmath import nan

import pytest

@pytest.fixture()
def my_dict():
    return {
        'Статус': ['Готов', 'В работе', 'В очереди'],
        'Номер': [1, 2, 3],
        'Источник': ['Зал', 'Телефон', 'Онлайн']
    }

@pytest.fixture()
def my_dict_transactions():
    return {
        "Дата операции": ['5', '6', '7', '8'],
        "Сумма операции": [1.2, -2.3, -3.4, 4.3],
        "Статус": ['OK', 'OK', 'FAILED', 'OK'],
        "Описание": ['топ', 'мидл', 'лоу', 'хайт'],
        "Категория": ['товар', nan, 'перевод', 'товар'],
        "Номер карты": ['*4556', '*7197', '*4556', '*7197']
    }

@pytest.fixture()
def my_dick_settings():
    return {
        'user_currencies': ['EUR'],
        'user_stocks': ['AMZN']
    }
