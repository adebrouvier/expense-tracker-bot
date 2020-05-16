import os
from dotenv import load_dotenv


class Config:

    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.sheet_name = os.getenv("SHEET_NAME")
        self.sheets_oauth = os.getenv("SHEETS_OAUTH")
        self.user_id = int(os.getenv("USER_ID"))
