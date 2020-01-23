import unittest
from tracker.google_sheet_editor import GoogleSheetEditor


class TestGoogleSheetEditor(unittest.TestCase):

    def test_range(self):
        editor = GoogleSheetEditor("Sheet", "credentials")
        assert editor.get_sheet('22-1-2020') == 'jan 20'
