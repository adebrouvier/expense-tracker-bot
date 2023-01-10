import logging
from datetime import date
from datetime import datetime
from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from sentry_sdk import capture_exception
from pygsheets.spreadsheet import WorksheetNotFound
from pygsheets.exceptions import SpreadsheetNotFound
import numpy as np
import sentry_sdk
from tracker.expense import Expense
from tracker.expense_tracker import ExpenseTracker
from tracker.config import Config
from tracker.google_sheet_editor import GoogleSheetEditor


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I'm the expense tracker bot")


def add(update, context):
    raw_date = " ".join(context.args)

    if not raw_date.strip():
        context.user_data['expense_date'] = date.today()
    else:
        try:
            parsed_date = datetime.strptime(raw_date, '%d/%m/%Y')
            context.user_data['expense_date'] = parsed_date
        except ValueError:
            update.message.reply_text("Invalid date provided. Expected format: dd/mm/yyyy")
            return ConversationHandler.END

    update.message.reply_text('Please send a *description*\.',
                              parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=ReplyKeyboardRemove())
    return DESCRIPTION


def description(update, context):
    text = update.message.text
    context.user_data['description'] = text
    logger.info("The description is %s", context.user_data['description'])
    update.message.reply_text('Please send the *location*\.',
                              parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=ReplyKeyboardRemove())
    return LOCATION


def location(update, context):
    text = update.message.text
    context.user_data['location'] = text
    logger.info("Location of expense: %s", update.message.text)
    update.message.reply_text('Please send the *price*\.',
                              parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=ReplyKeyboardRemove())
    return PRICE


def price(update, context):
    text = update.message.text
    context.user_data['price'] = int(text)
    logger.info("Price of expense: %s", update.message.text)

    category_keyboard = [x.tolist() for x in np.array_split(expense_tracker.get_categories(), 3)]
    update.message.reply_text('Please send the *category*\.',
                              parse_mode=ParseMode.MARKDOWN_V2,
                              reply_markup=ReplyKeyboardMarkup(category_keyboard,
                                                               one_time_keyboard=True))
    return CATEGORY


def category(update, context):
    text = update.message.text
    logger.info("Category of expense: %s", update.message.text)
    context.user_data['category'] = text

    expense = create_expense(context.user_data)
    try:
        expense_tracker.add_expense(expense)
        update.message.reply_text('Expense added ✅\n{}'.format(expense.to_markdown()),
                                  parse_mode=ParseMode.MARKDOWN_V2)
    except SpreadsheetNotFound:
        update.message.reply_text('Spreadsheet not found. Please update config variable.')
    except WorksheetNotFound:
        update.message.reply_text('Worksheet not found. Check if spreadsheet has worksheet for current month and year.')
    except Exception as error:
        update.message.reply_text('There was an error while adding the expense.')
        logger.error(error)
        capture_exception(error)

    return ConversationHandler.END


def cancel(update, _context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Expense canceled',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def create_expense(user_data):
    expense = Expense(user_data['expense_date'], user_data['description'], user_data['location'],
                      user_data['price'], user_data['category'])
    return expense


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

editor = GoogleSheetEditor(config.spreadsheet_name, config.sheets_oauth)
if config.development:
    editor.authorize_with_file()
else:
    editor.authorize_with_env_variable('GDRIVE_API_CREDENTIALS')
expense_tracker = ExpenseTracker(editor)


def main():
    logger.info("Starting bot...")
    updater = Updater(token=config.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start, Filters.user(user_id=config.user_id))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler())
    if config.development:
        logger.info("Starting in development mode")
        updater.start_polling()
    else:
        logger.info("Starting in production mode")
        webhook_url = "{}/{}".format(config.app_url, config.bot_token)
        updater.start_webhook(listen="0.0.0.0",
                              port=config.port,
                              url_path=config.bot_token,
                              webhook_url=webhook_url)
        logger.info("Started webhook in app {}".format(config.app_url))
        updater.idle()
    logger.info("Bot started.")


def conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('add', add, Filters.user(user_id=config.user_id))],

        states={
            DESCRIPTION: [MessageHandler(Filters.text, description)],

            LOCATION: [MessageHandler(Filters.text, location)],

            PRICE: [MessageHandler(Filters.regex(price_regex()), price)],

            CATEGORY: [MessageHandler(Filters.regex(categories_regex(expense_tracker)), category)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


def price_regex():
    return r'^[0-9]+$'


def categories_regex(expense_tracker):
    return '^({})$'.format('|'.join(expense_tracker.get_categories()))


if __name__ == '__main__':
    main()
