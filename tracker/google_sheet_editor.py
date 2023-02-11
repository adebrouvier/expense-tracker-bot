import logging
from datetime import date
from pygsheets.cell import Cell
from pygsheets.worksheet import Worksheet
from tracker.google_sheet_client import GoogleSheetClient


class GoogleSheetEditor:
    EXPENSE_COLUMN = "C"
    TYPE_COLUMN = "F"

    def __init__(self, spreadsheet: str, client: GoogleSheetClient):
        self.logger = logging.getLogger(__name__)
        self.spreadsheet = spreadsheet
        self.client = client

    @staticmethod
    def get_worksheet_name(date) -> str:
        return date.strftime('%b %y').lower()

    def open_worksheet(self, worksheet_title) -> Worksheet:
        return self.client.open(self.spreadsheet).worksheet_by_title(worksheet_title)

    def add_expense(self, worksheet: Worksheet, expense):
        cell = self.find_cell_by_date(worksheet, expense.spent_at)
        row = cell.row
        expense_values = expense.to_values()
        range_to_edit = self.cell_range(
            self.EXPENSE_COLUMN + str(row),
            self.end_column(expense_values) + str(row)
        )
        cell_list = worksheet.range(range_to_edit)[0]
        self.logger.debug("Processing values: {}".format(expense))
        if self.is_row_empty(cell_list):
            worksheet.update_values(self.EXPENSE_COLUMN + str(row), [expense_values])
        else:
            expense_values.insert(0, "")
            expense_values.insert(0, "")
            worksheet.insert_rows(row, number=1, values=expense_values)
        self.logger.debug("Added value to row with {} cell".format(expense.spent_at))

    def end_column(self, expense_values):
        return chr(ord(self.EXPENSE_COLUMN) + len(expense_values) - 1)

    def find_cell_by_date(self, worksheet: Worksheet, cell_date: date) -> Cell:
        return worksheet.find(self.formated_date(cell_date))[0]

    def get_cells(self, expense_date: date, worksheet: Worksheet) -> list:
        cell = self.find_cell_by_date(worksheet, expense_date)
        cell_matrix = worksheet.get_values(
            start='A2',
            end=self.TYPE_COLUMN + str(cell.row),
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
        )
        return cell_matrix

    @staticmethod
    def formated_date(expense_date: date):
        return '{dt.day}-{dt.month}-{dt.year}'.format(dt=expense_date)

    @staticmethod
    def cell_range(start: str, end: str):
        return start + ":" + end

    @staticmethod
    def is_row_empty(cell_list):
        for cell in cell_list:
            if cell.value != '':
                return False
        return True
