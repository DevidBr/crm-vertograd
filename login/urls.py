from django.urls import path
from login.views import main, log_out

app_name = 'login'

urlpatterns = [
    path('', main, name="main"),
    path('logout', log_out, name="logout")
]
