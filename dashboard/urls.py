from django.urls import path
from dashboard.views import home_dashboard, access_denied

app_name = "dashboard"

urlpatterns = [
    path("", home_dashboard, name="home_dashboard"),
    path("access_denied/", access_denied, name="access_denied")
]