import os

from src.services import investment_bank, preparing_list_transactions
from src.utils import read_xlsx_file
from src.views import main_page

path_to_xlsx_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.xlsx')

if __name__ == "__main__":
    print(main_page('2025-06-27 10:24:00'))
    print(investment_bank("2020-08", preparing_list_transactions(read_xlsx_file(path_to_xlsx_file)),50))