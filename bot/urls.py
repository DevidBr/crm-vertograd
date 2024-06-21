from django.urls import path
from bot.views import TestBotView, bot_test_send_message

app_name = 'bot'


urlpatterns = [
    path('test/', TestBotView.as_view(), name='test_bot'),
    path('test/send-message/', bot_test_send_message, name='bot_test_send_message')
]