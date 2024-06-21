from django.contrib import admin
from clients.models import Client, ContactPerson


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    pass
