
from django.contrib import admin
from .models import Food, Cart, CartItem, Order

admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)

