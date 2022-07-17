from django.contrib import admin
from .models import Coffee


# Register your models here.

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'payment_id', 'paid']
