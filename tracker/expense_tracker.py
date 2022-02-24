from tracker.google_sheet_editor import GoogleSheetEditor


class ExpenseTracker:

    def __init__(self, editor):
        self.editor = editor

    def add_expense(self, expense):
        worksheet_title = self.editor.get_worksheet_name(expense.date)
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
        return [row[0] for row in categories_matrix] # Extract column from matrix
