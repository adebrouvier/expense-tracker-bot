from datetime import date
from tracker.expense import Expense
from tracker.google_sheet_editor import GoogleSheetEditor
from pygsheets.spreadsheet import WorksheetNotFound


class ExpenseTracker:

    def __init__(self, editor: GoogleSheetEditor):
        self.editor = editor

    def add_expense(self, expense: Expense):
        worksheet_title = self.editor.get_worksheet_name(expense.spent_at)
        try:
            worksheet = self.editor.open_worksheet(worksheet_title)
            self.editor.add_expense(worksheet, expense)
        except WorksheetNotFound:
            msg = 'Worksheet {} for expense with date {} not found in spreadsheet.'.format(worksheet_title, str(expense.spent_at))
            raise WorksheetNotFound(msg)

    def get_categories(self):
        worksheet = self.editor.open_worksheet('non-fixed categories')
        categories_matrix = worksheet.get_values(
            start='B3',
            end='B99',
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
        )
        return [row[0] for row in categories_matrix]  # Extract column from matrix

    def last_expenses(self, number: int = 0) -> list[Expense]:
        '''
        Gets the last n expenses.

        number -- the number of expenses to obtain.
        '''
        current_date = date.today()
        worksheet_title = self.editor.get_worksheet_name(current_date)
        worksheet = self.editor.open_worksheet(worksheet_title)
        expenses_matrix = self.editor.get_cells(current_date, worksheet)

        filtered = filter(lambda expense: len(expense) > 3, expenses_matrix)

        expenses = map(lambda row: Expense(spent_at=row[0], description=row[2], location=row[3],
                                           price=row[4], category=row[5]), filtered)

        return list(expenses)[-number:]

    def last_expenses_as_markdown(self, number: int = 0) -> list[str]:
        '''
        Gets the last n expenses in markdown format.

        number -- the number of expenses to obtain.
        '''
        return [expense.to_markdown() for expense in self.last_expenses(number)]

    def total_expenses(self) -> int:
        '''
        Gets the sum of expense for the current month.
        '''
        expenses = self.last_expenses()
        return sum(int(expense.price) for expense in expenses)
