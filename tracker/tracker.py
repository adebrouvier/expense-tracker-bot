import logging
from datetime import date
from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from sentry_sdk import capture_exception
import numpy as np
import sentry_sdk
from tracker.expense import Expense
from tracker.google_sheet_editor import GoogleSheetEditor
from tracker.config import Config


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I'm the expense tracker bot")


def add(update, _context):
    update.message.reply_text('Please send a *description*.',
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardRemove())
    return DESCRIPTION


def description(update, context):
    text = update.message.text
    context.user_data['description'] = text
    logger.info("The description is %s", context.user_data['description'])
    update.message.reply_text('Please send the *location*.',
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardRemove())
    return LOCATION


def location(update, context):
    text = update.message.text
    context.user_data['location'] = text
    logger.info("Location of expense: %s", update.message.text)
    update.message.reply_text('Please send the *price*.',
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardRemove())
    return PRICE


def price(update, context):
    text = update.message.text
    context.user_data['price'] = int(text)
    logger.info("Price of expense: %s", update.message.text)

    category_keyboard = [x.tolist() for x in np.array_split(categories(), 3)]
    update.message.reply_text('Please send the *category*.',
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup(category_keyboard,
                                                               one_time_keyboard=True))
    return CATEGORY


def category(update, context):
    text = update.message.text
    logger.info("Category of expense: %s", update.message.text)
    context.user_data['category'] = text

    expense = create_expense(context.user_data, date.today())
    try:
        add_expense(expense)
        update.message.reply_text('Expense added: {}'.format(str(expense)))
    except Exception as error:
        update.message.reply_text('There was an error while adding the expense.')
        capture_exception(error)

    return ConversationHandler.END


def cancel(update, _context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Expense canceled',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def create_expense(user_data, expense_date):
    expense = Expense(expense_date, user_data['description'], user_data['location'],
                      user_data['price'], user_data['category'])
    return expense


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

DESCRIPTION, LOCATION, PRICE, CATEGORY = range(4)

config = Config()

sentry_sdk.init(
    config.sentry_dsn,
    traces_sample_rate=1.0
)


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
        updater.start_webhook(listen="0.0.0.0",
                              port=config.port,
                              url_path=config.bot_token)
        webhook_url = "https://{}.herokuapp.com/{}".format(config.app_name, config.bot_token)
        updater.bot.set_webhook(webhook_url)
        updater.idle()
    logger.info("Bot started.")


def conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('add', add, Filters.user(user_id=config.user_id))],

        states={
            DESCRIPTION: [MessageHandler(Filters.text, description)],

            LOCATION: [MessageHandler(Filters.text, location)],

            PRICE: [MessageHandler(Filters.regex(r'\d+'), price)],

            CATEGORY: [MessageHandler(Filters.regex(categories_regex()), category)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


def add_expense(expense):
    editor = GoogleSheetEditor(config.spreadsheet_name, config.sheets_oauth)
    if config.development:
        client = editor.authorize_with_file()
    else:
        client = editor.authorize_with_env_variable('GDRIVE_API_CREDENTIALS')
    worksheet_title = editor.get_worksheet_name(expense.date)
    worksheet = editor.open_worksheet(client, worksheet_title)
    editor.add_expense(worksheet, expense)


def categories_regex():
    return '^({})$'.format('|'.join(categories()))


def categories():
    return ["Comida", "Entretenimiento", "Electronics/Gadgets", "Transporte", "Ropa", "Inversiones",
            "Medical", "Otros"]


if __name__ == '__main__':
    main()
