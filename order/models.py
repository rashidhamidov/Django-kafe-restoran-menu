from django.db import models
from django.contrib.auth.models import User
from menu.models import Urun
from django.forms import ModelForm, TextInput, Textarea,widgets
from django.contrib.auth.models import User
# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    urun = models.ForeignKey(Urun,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    def __str__(self):
        return self.urun.title

    @property
    def amount(self):
        return (self.quantity*self.urun.price)

    @property
    def price(self):
        return (self.urun.price)


class ShopCartForm(ModelForm):
    class Meta:
        model=ShopCart
        fields=['quantity']

class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Onaylandı','Onaylandı'),
        ('Yapılıyor','Yapılıyor'),
        ('Çıkarıldı','Çıkarıldı'),
        ('Masada','Masada'),
        ('İptal','İptal'),

    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    masa = models.CharField (blank=True,max_length=20,editable=False)
    total= models.FloatField()
    ip = models.CharField(blank=True,max_length=20)
    status= models.CharField (blank=True,max_length=15, choices=STATUS)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)

    def __str__ (self):
        return self.masa

class OrderProduct(models.Model):
    STATUS=(
        ('New','New'),
        ('Onaylandı','Onaylandı'),
        ('Yapılıyor','Yapılıyor'),
        ('Çıkarıldı','Çıkarıldı'),
        ('Masada','Masada'),
        ('İptal','İptal'),

    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    urun = models.ForeignKey(Urun,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    amount=models.FloatField()
    status= models.CharField (blank=True,max_length=15, choices=STATUS)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)

    def __str__(self):
        return self.urun.title


