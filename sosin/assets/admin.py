from django.contrib import admin
from .models import Assets

# Register your models here.
@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid')