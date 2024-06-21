import os
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

bot = TeleBot(token=os.getenv("TELEGRAM_TOKEN"))


