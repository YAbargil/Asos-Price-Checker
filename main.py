from telegram.ext import *
import Constants as keys
import Responses as R


def start_command(update, context):
    update.message.reply_text("Enter the URL")


def handle_message(update,context):
    text = str(update.message.text)
    price = R.checkItem(text)

    for msg in price:
        update.message.reply_text(msg)


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

main()
