from django.contrib import admin
from .models import ShopCart,Urun,Order,OrderProduct
from django import forms
# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','urun','price','quantity','amount']
    list_filter = ['user']
class OrderProductLine(admin.TabularInline):
    model=OrderProduct
    readonly_fields = ['user','urun','price','quantity','amount']
    can_delete=False
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['masa','user','status','total','update_at']
    list_filter = ['masa']
    readonly_fields=('masa','user','total','update_at','create_at')
    inlines=[OrderProductLine]

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)