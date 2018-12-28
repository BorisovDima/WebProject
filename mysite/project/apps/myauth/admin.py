from django.contrib import admin

from .models import BanListAdmin, BanList
# Register your models here.

admin.site.register(BanList, BanListAdmin)