from django.contrib import admin

from login.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
