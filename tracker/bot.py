import locale
import logging
from datetime import date
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from sentry_sdk import capture_exception
from pygsheets.spreadsheet import WorksheetNotFound
from pygsheets.exceptions import SpreadsheetNotFound
import numpy as np
import sentry_sdk
from tracker.expense import Expense
from tracker.expense_tracker import ExpenseTracker
from tracker.config import Config
from tracker.google_sheet_client import GoogleSheetClient
from tracker.google_sheet_editor import GoogleSheetEditor


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi! I'm the expense tracker bot")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_date = " ".join(context.args)

    if not raw_date.strip():
        context.user_data['expense_date'] = date.today()
    else:
        try:
            parsed_date = datetime.strptime(raw_date, '%d/%m/%Y')
            context.user_data['expense_date'] = parsed_date
        except ValueError:
            await update.message.reply_text("Invalid date provided. Expected format: dd/mm/yyyy")
            return ConversationHandler.END

    await reply_message(update, 'Please send a *description*\\.', ReplyKeyboardRemove())
    return DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data['description'] = text
    logger.info("The description is %s", context.user_data['description'])
    await reply_message(update, 'Please send the *location*\\.', ReplyKeyboardRemove())
    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data['location'] = text
    logger.info("Location of expense: %s", update.message.text)
    await reply_message(update, 'Please send the *price*\\.', ReplyKeyboardRemove())
    return PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data['price'] = int(text)
    logger.info("Price of expense: %s", update.message.text)

    category_keyboard = [x.tolist() for x in np.array_split(expense_tracker.get_categories(), 3)]
    await reply_message(update, 'Please send the *category*\\.',
                        ReplyKeyboardMarkup(category_keyboard, one_time_keyboard=True))
    return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logger.info("Category of expense: %s", update.message.text)
    context.user_data['category'] = text

    expense = create_expense(context.user_data)
    try:
        expense_tracker.add_expense(expense)
        await reply_message(update, 'Expense added ✅\n{}'.format(expense.to_markdown()))
    except SpreadsheetNotFound:
        await update.message.reply_text('Spreadsheet not found. Please update config variable.')
    except WorksheetNotFound as error:
        await update.message.reply_text(str(error))
    except Exception as error:  # pylint: disable=broad-except
        await update.message.reply_text('There was an error while adding the expense.')
        logger.error(error)
        capture_exception(error)

    return ConversationHandler.END


async def cancel(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.from_user:
        user_name = update.message.from_user
    logger.info("User %s canceled the conversation.", user_name)
    await reply_message(update, 'Expense canceled', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def last_expenses(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    number_of_expenses = 5
    last_expenses = expense_tracker.last_expenses_as_markdown(number_of_expenses)
    await reply_message(update, 'Last {} expenses\n{}'.format(number_of_expenses, '\n\n'.join(last_expenses)))
    return ConversationHandler.END

async def total_expenses(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    total_expenses = expense_tracker.total_expenses()
    await reply_message(update, 'Total expenses: {}'.format(locale.currency(total_expenses, grouping=True)))
    return ConversationHandler.END


def create_expense(user_data) -> Expense:
    expense = Expense(user_data['expense_date'], user_data['description'], user_data['location'],
                      user_data['price'], user_data['category'])
    return expense


async def reply_message(update: Update, text: str, reply_markup=None):
    await update.message.reply_text(text,
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    reply_markup=reply_markup)

def get_spreadsheet_name_with_suffix(spreadsheet_name_suffix: str) -> str:
    current_year = date.today().year
    return f"{str(current_year)} {spreadsheet_name_suffix}"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

DESCRIPTION, LOCATION, PRICE, CATEGORY = range(4)

config = Config()

sentry_sdk.init(
    config.sentry_dsn,
    traces_sample_rate=1.0,
    environment='production' if not config.development else 'development',
)

locale.setlocale(locale.LC_ALL, config.locale)

client = GoogleSheetClient(config.sheets_oauth, 'GDRIVE_API_CREDENTIALS')
if config.development:
    client.authorize_with_file()
else:
    client.authorize_with_env_variable()

if config.spreadsheet_name_suffix:
    spreadsheet_name = get_spreadsheet_name_with_suffix(config.spreadsheet_name_suffix)
else:
    spreadsheet_name = config.spreadsheet_name

editor = GoogleSheetEditor(spreadsheet_name, client)
expense_tracker = ExpenseTracker(editor)


def main() -> None:
    logger.info("Starting bot...")
    application = ApplicationBuilder().token(config.bot_token).build()
    start_handler = CommandHandler('start', start, filters.User(user_id=config.user_id))
    application.add_handler(start_handler)
    application.add_handler(conversation_handler())

    if config.development:
        logger.info("Starting in development mode")
        application.run_polling()
    else:
        logger.info("Starting in production mode")
        webhook_url = "{}/{}".format(config.app_url, config.bot_token)
        application.run_webhook(listen="0.0.0.0",
                                port=config.port,
                                url_path=config.bot_token,
                                webhook_url=webhook_url)
        logger.info("Started webhook in app %s", config.app_url)


def conversation_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler('add', add, filters.User(user_id=config.user_id)),
            CommandHandler('last', last_expenses, filters.User(user_id=config.user_id)),
            CommandHandler('total', total_expenses, filters.User(user_id=config.user_id))
        ],

        states={
            DESCRIPTION: [MessageHandler(filters.TEXT, description)],

            LOCATION: [MessageHandler(filters.TEXT, location)],

            PRICE: [MessageHandler(filters.Regex(price_regex()), price)],

            CATEGORY: [MessageHandler(filters.Regex(categories_regex(expense_tracker)), category)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


def price_regex():
    return r'^[0-9]+$'


def categories_regex(tracker):
    return '^({})$'.format('|'.join(tracker.get_categories()))


if __name__ == '__main__':
    main()
