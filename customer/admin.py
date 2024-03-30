from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "phoneNumber"]

admin.site.register(Contact, ContactAdmin)
