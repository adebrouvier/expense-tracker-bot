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
from tracker.expense import Expense
from tracker.google_sheet_editor import GoogleSheetEditor
import numpy as np
import tracker.config as config


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
    context.user_data['price'] = text
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
    add_expense(expense)
    update.message.reply_text('Adding expense {}'.format(str(expense)))
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


def main():
    logger.info("Starting bot...")
    updater = Updater(token=config.bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add, Filters.user(user_id=config.user_id))],

        states={
            DESCRIPTION: [MessageHandler(Filters.text, description)],

            LOCATION: [MessageHandler(Filters.text, location)],

            PRICE: [MessageHandler(Filters.text, price)],

            CATEGORY: [MessageHandler(Filters.regex('^({})$'.format('|'.join(categories()))), category)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    start_handler = CommandHandler('start', start, Filters.user(user_id=config.user_id))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    logger.info("Bot started.")

def add_expense(expense):
    editor = GoogleSheetEditor(config.sheet_name, config.sheets_oauth)
    client = editor.authorize()
    sheet = editor.get_sheet(expense.date)
    worksheet = editor.open_worksheet(client, sheet)
    editor.add_expense(worksheet, expense)

def categories():
    return ["Comida", "Entretenimiento", "Electronics/Gadgets", "Transporte", "Ropa", "Inversiones", "Medical", "Otros"]

if __name__ == '__main__':
    main()
