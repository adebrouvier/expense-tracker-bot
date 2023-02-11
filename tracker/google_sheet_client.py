from pygsheets import authorize
from pygsheets.client import Client
from pygsheets.spreadsheet import Spreadsheet


class GoogleSheetClient:

    def __init__(self, credentials_path: str, service_account_env_var):
        self.credentials_path = credentials_path
        self.service_account_env_var = service_account_env_var
        self.client = None

    def authorize_with_file(self) -> Client:
        self.client = authorize(service_account_file=self.credentials_path)

    def authorize_with_env_variable(self) -> Client:
        self.client = authorize(service_account_env_var=self.service_account_env_var)

    def open(self, spreadsheet: str) -> Spreadsheet:
        return self.client.open(spreadsheet)
