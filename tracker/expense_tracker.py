from datetime import date
from tracker.expense import Expense
from tracker.google_sheet_editor import GoogleSheetEditor


class ExpenseTracker:

    def __init__(self, editor: GoogleSheetEditor):
        self.editor = editor

    def add_expense(self, expense):
        worksheet_title = self.editor.get_worksheet_name(expense.spent_at)
        worksheet = self.editor.open_worksheet(worksheet_title)
        self.editor.add_expense(worksheet, expense)

    def get_categories(self):
        worksheet = self.editor.open_worksheet('non-fixed categories')
        categories_matrix = worksheet.get_values(
            start='B3',
            end='B99',
            include_tailing_empty=False,
            include_tailing_empty_rows=False,
        )
        return [row[0] for row in categories_matrix]  # Extract column from matrix

    def last_expenses(self, number: int):
        current_date = date.today()
        worksheet_title = self.editor.get_worksheet_name(current_date)
        worksheet = self.editor.open_worksheet(worksheet_title)
        expenses_matrix = self.editor.get_cells(current_date, worksheet)

        filtered = filter(lambda expense: len(expense) > 3, expenses_matrix)

        expenses = map(lambda row: Expense(spent_at=row[0], description=row[2], location=row[3],
                                           price=row[4], category=row[5]).to_markdown(), filtered)

        return list(expenses)[-number:]
