import pygsheets


class GoogleSheetEditor:
    EXPENSE_START_COLUMN = "C"

    def __init__(self, spreadsheet, credentials_path):
        self.spreadsheet = spreadsheet
        self.credentials_path = credentials_path

    def authorize_with_file(self):
        self.client = pygsheets.authorize(service_file=self.credentials_path)

    def authorize_with_env_variable(self, env_var):
        self.client = pygsheets.authorize(service_account_env_var=env_var)

    @staticmethod
    def get_worksheet_name(date):
        return date.strftime('%b %y').lower()

    def open_worksheet(self, worksheet_title):
        return self.client.open(self.spreadsheet).worksheet_by_title(worksheet_title)

    def add_expense(self, worksheet, expense):
        cell = worksheet.find(self.formated_date(expense.date))[0]
        row = cell.row
        expense_values = expense.to_values()
        range_to_edit = self.cell_range(
            self.EXPENSE_START_COLUMN + str(row),
            self.end_column(expense_values) + str(row)
        )
        cell_list = worksheet.range(range_to_edit)[0]
        print("Processing expense: {}".format(expense))
        if self.row_empty(cell_list):
            worksheet.update_values(self.EXPENSE_START_COLUMN + str(row), [expense_values])
        else:
            expense_values.insert(0, "")
            expense_values.insert(0, "")
            worksheet.insert_rows(cell.row, number=1, values=expense_values)
        print("Added expense for {}".format(expense.date))

    def end_column(self, expense_values):
        return chr(ord(self.EXPENSE_START_COLUMN) + len(expense_values) - 1)

    @staticmethod
    def formated_date(date):
        return '{dt.day}-{dt.month}-{dt.year}'.format(dt=date)

    @staticmethod
    def cell_range(start, end):
        return start + ":" + end

    @staticmethod
    def row_empty(cell_list):
        for cell in cell_list:
            if cell.value != '':
                return False
        return True
