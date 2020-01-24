import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GoogleSheetEditor:

    def __init__(self, sheet, credentials_path):
        self.sheet = sheet
        self.credentials_path = credentials_path

    def authorize(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_path, scope
        )
        client = gspread.authorize(credentials)
        return client

    @staticmethod
    def get_sheet(date):
        return date.strftime('%b %y').lower()

    def open_worksheet(self, client, sheet):
        return client.open(self.sheet).worksheet(sheet)

    def add_expense(self, worksheet, expense):
        cell = worksheet.find(self.formated_date(expense.date))
        row = cell.row
        range_to_edit = self.cell_range("C" + str(row), "F" + str(row))
        cell_list = worksheet.range(range_to_edit)
        expense_values = expense.to_values()
        print("Processing expense: {}".format(expense))
        if self.row_empty(cell_list):
            for index, cell in enumerate(cell_list):
                cell.value = expense_values[index]
            worksheet.update_cells(cell_list)
        else:
            expense_values.insert(0, "")
            expense_values.insert(0, "")
            worksheet.insert_row(expense_values, cell.row + 1)
        print("Added expense for {}".format(expense.date))

    @staticmethod
    def formated_date(date):
        return '{dt.day}-{dt.month}-{dt.year}'.format(dt = date)

    @staticmethod
    def cell_range(start, end):
        return start + ":" + end

    @staticmethod
    def row_empty(cell_list):
        for cell in cell_list:
            if cell.value != '':
                return False
        return True
