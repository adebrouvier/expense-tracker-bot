import unittest
from tracker.google_sheet_editor import GoogleSheetEditor


class TestGoogleSheetEditor(unittest.TestCase):

    def test_range(self):
        editor = GoogleSheetEditor("Sheet", "credentials")
        self.assertEqual('jan 20', editor.get_sheet('22-1-2020'))


if __name__ == '__main__':
    unittest.main()
