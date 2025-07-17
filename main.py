import os

from src.reports import spending_by_category
from src.services import investment_bank, preparing_list_transactions
from src.utils import read_xlsx_file
from src.views import main_page

path_to_xlsx_file = os.path.join(os.path.dirname(__file__), 'data', 'operations.xlsx')

if __name__ == "__main__":

    while True:

        user_choice_page = int(input(
"""Выберите нужную функциональность.
1. Веб-страницы:
    -Главная
2. Сервисы:
    -Инвесткопилка
3. Отчет
    -Траты по категории
"""

'\nВвод: ')
        )

        if user_choice_page == 1:
            print(
                main_page(
                    input("Введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС, "
                          "до которой вы хотите получить анализ в этом месяце\nВвод: ")
                )
            )
            break
        if user_choice_page == 2:
            print(
                investment_bank(
                    input("Укажите месяц в формате ГГГГ-ММ, для которого вы хотите получить расчет\nВвод: "),
                    preparing_list_transactions(read_xlsx_file(path_to_xlsx_file)),
                    int(input("Введите порог округления, для расчета накоплений. "
                              "Доступные варианты 10, 50, 100\nВвод: "))
                )
            )
            break
        if user_choice_page == 3:
            print(
                spending_by_category(
                    read_xlsx_file(path_to_xlsx_file),
                    input("Укажите категорию по которой вы хотите получить отчет\nВвод: "),
                    input("Укажите дату до которой нужно произвести расчеты в формате ДД-ММ-ГГГГ ЧЧ:ММ:СС "
                          "берутся 3 месяца до нее. "
                          "Либо оставьте поле пустым если нужен расчет до текущей даты.\nВвод: ")
                )
            )
            break
        else:
            print("Указан несуществующий пункт.")