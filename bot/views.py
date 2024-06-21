import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.views.generic import View
from bot.main_bot import bot


load_dotenv()


# TODO: удалить при деплое
class TestBotView(View):
    def get(self, request):
        return render(request, 'bot/test_bot.html')


# TODO: удалить при деплое
def bot_test_send_message(request):
    # Обычное сообщение для теста работы бота
    bot.send_message(chat_id=os.getenv("ADMIN_API"), text="Тест работы бота с сайта")
    return render(request, 'bot/test_bot.html')

