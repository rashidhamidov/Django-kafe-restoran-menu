from django.urls import path
from . import views


urlpatterns = [
  
    path('', views.index, name='index'),
    path('addurun/<int:id>',views.addurun,name='addurun'),
    path('shopcart/',views.shopcart,name='shopcart'),
    path('deletefromcart/<int:id>',views.deletefromcart,name='deletefromcart'),
    path('siparis/',views.siparis,name='siparis')
]