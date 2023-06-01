import unittest
from tracker.google_sheet_client import GoogleSheetClient
from unittest.mock import MagicMock

class TestGoogleSheetClient(unittest.TestCase):

    def test_open_raises_error_if_unauthorized(self):
        client = MagicMock()
        editor = GoogleSheetClient("Sheet", client)
        with self.assertRaisesRegex(Exception, 'Client must be authorized before calling open'):
            editor.open("Spreadsheet")