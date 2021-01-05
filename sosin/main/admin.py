from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Coins)
class MainAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

@admin.register(Stocks)
class MainAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')

@admin.register(News)
class MainAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')