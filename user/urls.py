from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update,name='user_update'),
    path('password/', views.change_password,name='change_password'),
    path('comments/', views.comments,name='comments'),
    path('orders/', views.orders,name='orders'),
    path('deletecomment/<int:id>', views.deletecomment,name='deletecomment'),
    path('orderdetail/<int:id>', views.orderdetail,name='orderdetail'),
]