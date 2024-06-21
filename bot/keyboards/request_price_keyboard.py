from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton as bt

request_price_keyboard = InlineKeyboardMarkup()
btn_1 = bt(text="Написать себестоимость и одобрить", callback_data="request_data")

confirmation = request_price_keyboard.row(btn_1)
