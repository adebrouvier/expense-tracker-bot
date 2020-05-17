from datetime import date
from tracker.google_sheet_editor import GoogleSheetEditor


class TestGoogleSheetEditor():

    def test_get_sheet_name(self):
        editor = GoogleSheetEditor("Sheet", "credentials")
        assert editor.get_worksheet_name(date(2020, 1, 13)) == 'jan 20'

    def test_formated_date(self):
        editor = GoogleSheetEditor("Sheet", "credentials")
        assert editor.formated_date(date(2020, 1, 13)) == '13-1-2020'

    def test_end_column(self):
        editor = GoogleSheetEditor("Sheet", "credentials")
        assert editor.end_column([1, 2, 3, 4]) == 'F'
