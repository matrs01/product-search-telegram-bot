import telebot
from gc import callbacks
from telebot import types

from telegram_bot import config as cfg
from shop_parser import MVideo, Wildberries, Item

'''
This bot searches for products in online shops (available now: Wildberries and MVideo).
Send /start to start a new search.
'''


bot = telebot.TeleBot(cfg.TOKEN)


@bot.message_handler(commands=["start", "help"])
def describe(message: telebot.types.Message):
    bot.send_message(
        message.chat.id, "Hi! Here you can search for the items you are looking for. Specify the product.")


@bot.message_handler(content_types=["text"])
def choose_shop(message: telebot.types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mvideo_button = types.KeyboardButton(cfg.MVIDEO_BUTTON)
    wb_button = types.KeyboardButton(cfg.WB_BUTTON)
    all_button = types.KeyboardButton(cfg.ALL_BUTTON)
    keyboard.row(mvideo_button, wb_button)
    keyboard.row(all_button)

    query = message.text

    message = bot.send_message(
        chat_id=message.chat.id,
        text="Select shop:",
        reply_markup=keyboard
    )

    bot.register_next_step_handler(
        message, callback=callback_worker, query=query)


def callback_worker(message: telebot.types.Message, query):
    if message.text == cfg.MVIDEO_BUTTON:
        item_list = MVideo.parse_items(query)
        send_items(message, item_list)
    elif message.text == cfg.WB_BUTTON:
        item_list = Wildberries.parse_items(query)
        send_items(message, item_list)
    elif message.text == cfg.ALL_BUTTON:
        try:
            mvideo_list = MVideo.parse_items(query, num=2)
        except:
            mvideo_list = []

        try:
            wb_list = Wildberries.parse_items(query, num=2)
        except:
            wb_list = []

        item_list = mvideo_list + wb_list
        send_items(message, item_list)

    elif any(greeting in message.text.lower() for greeting in cfg.GREETINGS):
        bot.send_message(
            message.chat.id, "Hi! Welcome to product search bot.")
    bot.send_message(
        message.chat.id, "Specify the product you are looking for.")


def send_items(message, item_list):
    if len(item_list) == 0:
        bot.send_message(
            message.chat.id, "Sorry, connection error. Try Again")
    else:
        for item in item_list:
            bot.send_photo(message.chat.id, item.pic,
                           caption=item.name + '\nPrice: ' + item.price + '\n' + item.ref)


if __name__ == '__main__':
    bot.infinity_polling()
