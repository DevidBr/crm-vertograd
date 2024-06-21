from django.urls import path
from clients.views import clients_main, add_client, client_detail, client_add_contact, contact_person_detail, \
    contact_person_change

app_name = "clients"

urlpatterns = [
    path("", clients_main, name="clients_main"),
    path("add/", add_client, name="add_client"),
    path("client_detail/<int:client_id>/", client_detail, name="client_detail"),
    path("client_add_contact/<int:client_id>/", client_add_contact, name="client_add_contact"),
    path("contact_persons/detail/<int:contact_person_id>/", contact_person_detail, name="contact_person_detail"),
    path("contact_persons/detail/change/<int:contact_person_id>/", contact_person_change, name="contact_person_change"),
]
