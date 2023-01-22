from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem

# Register your models here.

#class CartAdmin(admin.ModelAdmin):
#        prepopulated_fields = {'slug': ('cart_id',)}
#        list_display = ('product', 'quantity', 'date_add', 'category', 'modified_date', 'is_available')
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_add')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)