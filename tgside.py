import telebot
import os

from yamlparser import TGTOKEN

bot = telebot.TeleBot(TGTOKEN)


def send_message(message: str, chat_id):
    bot.send_message(chat_id, message, parse_mode="Markdown")


def send_photo(url: str, chat_id):
    bot.send_photo(chat_id, url)


def send_doc(name: str, chat_id):
    file = open(name, "rb")
    bot.send_document(chat_id, file)
    os.remove(f'{name}')

