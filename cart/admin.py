from django.contrib import admin
from .models import Order, Item

# Register your models here.
from .models import Order
admin.site.register(Order)
admin.site.register(Item)