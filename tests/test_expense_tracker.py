from unittest.mock import MagicMock
from unittest.mock import patch
from tracker.expense_tracker import ExpenseTracker
from tracker.google_sheet_editor import GoogleSheetEditor


class TestExpenseTracker():

    @patch('tracker.google_sheet_editor.GoogleSheetEditor.get_cells')
    def test_last_expenses_with_empty_row(self, get_cells_mock):
        get_cells_mock.return_value = [['22-1-2020', 'Day']]
        editor = MagicMock(spec=GoogleSheetEditor, get_cells=get_cells_mock)
        expense_tracker = ExpenseTracker(editor=editor)
        assert expense_tracker.last_expenses(1) == []

    @patch('tracker.google_sheet_editor.GoogleSheetEditor.get_cells')
    def test_last_expenses(self, get_cells_mock):
        get_cells_mock.return_value = [['22-1-2020', 'Friday', 'Burger', 'OutNIn', '10', 'Food'],
                                       ['23-1-2020', 'Saturday', 'Burger', 'OutNIn', '10', 'Food']]
        editor = MagicMock(spec=GoogleSheetEditor, get_cells=get_cells_mock)
        expense_tracker = ExpenseTracker(editor=editor)
        assert expense_tracker.last_expenses(1) == ['❗ *Description*: Burger\n' \
               + '📍 *Location*: OutNIn\n💰 *Price*: $10\n🏷 *Category*: Food\n' \
               + '📅 *Date*: 23\\-1\\-2020']
