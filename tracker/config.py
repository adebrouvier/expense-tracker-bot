import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.spreadsheet_name = os.getenv("SPREADSHEET_NAME")
        self.sheets_oauth = os.getenv("SHEETS_OAUTH")
        self.user_id = int(os.getenv("USER_ID"))
        self.development = os.getenv("DEVELOPMENT") == 'True'
        self.port = int(os.getenv("PORT", "8443"))
        self.app_name = os.getenv("APP_NAME")
        self.sentry_dsn = os.getenv("SENTRY_DSN")
