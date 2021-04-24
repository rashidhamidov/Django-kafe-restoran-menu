"""proje1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

from home import views


urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path('hakimizda/', views.hakimizda,name='hakimizda'),
    path('referans/', views.referans,name='referans'),
    path('iletisim/', views.iletisim,name='iletisim'),
    path('faq/', views.faq,name='faq'),
    path('menu/', include('menu.urls')),
    path('order/', include('order.urls')),


    path('categori/<int:id>/<slug:slug>', views.categori_products,name='categori_products'),
    path('search/', views.product_search,name='product_search'),
    path('logout/', views.logout_view,name='logout_view'),
    path('login/', views.login_view,name='login_view'),
    path('join/', views.join_view,name='join_view'),
    path('urun/<int:id>/<slug:slug>', views.urun_detay,name='urun_detay'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('content/<int:id>/<slug:slug>', views.content_detail, name='content_detail'),
]

if settings.DEBUG: # new
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

