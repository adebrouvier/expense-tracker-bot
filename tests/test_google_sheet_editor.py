from datetime import date
from tracker.google_sheet_editor import GoogleSheetEditor
from unittest.mock import MagicMock


class TestGoogleSheetEditor():

    def test_get_sheet_name(self):
        client = MagicMock()
        editor = GoogleSheetEditor("Sheet", client)
        assert editor.get_worksheet_name(date(2020, 1, 13)) == 'jan 20'

    def test_formated_date(self):
        client = MagicMock()
        editor = GoogleSheetEditor("Sheet", client)
        assert editor.formated_date(date(2020, 1, 13)) == '13-1-2020'

    def test_end_column(self):
        client = MagicMock()
        editor = GoogleSheetEditor("Sheet", client)
        assert editor.end_column([1, 2, 3, 4]) == 'F'

    def test_find_cell_by_date_raises_value_error_when_not_found(self):
        client = MagicMock()
        editor = GoogleSheetEditor("Sheet", client)
        worksheet = MagicMock()
        worksheet.find.return_value = []

        try:
            editor.find_cell_by_date(worksheet, date(2025, 1, 1))
            assert False, 'Expected ValueError'
        except ValueError as error:
            assert str(error) == 'No cell found for date: 2025-01-01'
