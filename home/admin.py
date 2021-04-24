from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Ayarlar,ContactFormMessage,UserProfile,FAQ

admin.site.register(Ayarlar)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','message','ip','note','status']
    list_filter=['status']
class UyeProfileAdmin(admin.ModelAdmin):
    list_display=['user_name','Full_name','phone','city','adress','image_tag','country']


class FAQAdmin(admin.ModelAdmin):
    list_display=['question','ordernumber','answer','status']
    list_filter=['status']

admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(UserProfile,UyeProfileAdmin)
admin.site.register(FAQ,FAQAdmin)