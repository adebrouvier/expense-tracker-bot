import pygsheets


class GoogleSheetEditor:

    def __init__(self, spreadsheet, credentials_path):
        self.spreadsheet = spreadsheet
        self.credentials_path = credentials_path

    def authorize(self):
        client = pygsheets.authorize(service_file=self.credentials_path)
        return client

    @staticmethod
    def get_worksheet_name(date):
        return date.strftime('%b %y').lower()

    def open_worksheet(self, client, worksheet_title):
        return client.open(self.spreadsheet).worksheet_by_title(worksheet_title)

    def add_expense(self, worksheet, expense):
        cell = worksheet.find(self.formated_date(expense.date))[0]
        row = cell.row
        range_to_edit = self.cell_range("C" + str(row), "F" + str(row))
        cell_list = worksheet.range(range_to_edit)[0]
        expense_values = expense.to_values()
        print("Processing expense: {}".format(expense))
        if self.row_empty(cell_list):
            for index, cell in enumerate(cell_list):
                cell.set_value(expense_values[index])
            worksheet.update_cells(cell_list)
        else:
            expense_values.insert(0, "")
            expense_values.insert(0, "")
            worksheet.insert_rows(cell.row + 1, number=1, values=expense_values)
        print("Added expense for {}".format(expense.date))

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
