from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import models
from home.forms import SearchForm
from home.models import Ayarlar,ContactFormu,ContactFormMessage
from django.contrib import messages
from menu.models import Categori,Urun,Images,Comment
from django.contrib.auth import authenticate, login, logout
import json
import random
from home.forms import Signupform
from home.models import UserProfile,FAQ
from order.models import ShopCart
from django.core.files import images


def index(request):
    current_user=request.user
    sliderdata=Urun.objects.filter(status=True,tip='Diger').order_by('title')[:6]
    kahvalti=(Urun.objects.filter(tip='Kahvalti',status=True)|Urun.objects.filter(tip='Haber',status=True)).order_by('-update_at')[:3]
    diger=Urun.objects.filter(status=True,tip='Diger').order_by('-update_at')
    icecek=Urun.objects.filter(status=True,tip='Icecek').order_by('-update_at')
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
        'ayar':ayar,
        'sliderdata':sliderdata,
        'categori':categori,
        'kahvalti':kahvalti,
        'icecek':icecek,
        'diger':diger,
        'menu':menu,
        'menu_icerik':menu_icerik,
    }
    
    request.session['cart_item']=ShopCart.objects.filter(user_id=current_user.id).count()
    return render(request, 'index.html',context)


def hakimizda(request):
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
                'ayar':ayar,
                'categori':categori,
                'menu':menu,
                'menu_icerik':menu_icerik,
                }
    return render(request, 'hakimizda.html',context)


def referans(request):
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
                'ayar':ayar,
                'categori':categori,
                'menu':menu,
                'menu_icerik':menu_icerik,
                }
    return render(request, 'referans.html',context)

def iletisim(request):

    if request.method == 'POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajiniz basariyla Gonderilmistir")
            return HttpResponseRedirect('/iletisim')
        
    form =ContactFormu()
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
        'ayar':ayar,
        'page':'iletisim',
        'categori':categori,
        'form':form,
        'menu':menu,
        'menu_icerik':menu_icerik,

            
    
    
    }
    return render(request, 'iletisim.html',context)

def categori_products(request,id,slug):
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    categoridata=Categori.objects.get(pk=id)
    parent_categori_id=Categori.objects.filter(tree_id=categoridata.tree_id,level=0)
    products=Urun.objects.filter(Categori_id=id,status=True)
    context={
        
        'ayar':ayar,
        'products':products,
        'categori':categori,
        'categoridata':categoridata,
        'parent_categori':parent_categori_id,
        'menu':menu,
        'menu_icerik':menu_icerik,

    }
    return render(request, 'products.html',context)
def urun_detay(request,id,slug):
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    products=Urun.objects.get(pk=id)
    images=Images.objects.filter(urun_id=id)
    comment=Comment.objects.filter(urun_id=id,status=True).order_by('-update_at')
    benzer=Urun.objects.filter(Categori_id=products.Categori_id,status=True)[:3]
    soneklenen=Urun.objects.filter(status=True).order_by('-update_at')[:10]
    context={
        'comment':comment,
        'ayar':ayar,
        'products':products,
        'categori':categori,
        'images':images,
        'benzer':benzer,
        'soneklenen':soneklenen,
        'menu':menu,
        'menu_icerik':menu_icerik,

    }
    return render(request, 'urun_detay.html',context)

def content_detail(request,id,slug):
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    products=Urun.objects.get(pk=id)
    images=Images.objects.filter(urun_id=id)
    comment=Comment.objects.filter(urun_id=id,status=True).order_by('-update_at')[:5]
    benzer=Urun.objects.filter(Categori_id=products.Categori_id,status=True)[:3]
    soneklenen=Urun.objects.filter(status=True,tip='Etkinlik').order_by('-update_at')[:3]
    context={
        'comment':comment,
        'ayar':ayar,
        'products':products,
        'categori':categori,
        'images':images,
        'benzer':benzer,
        'soneklenen':soneklenen,
        'menu':menu,
        'menu_icerik':menu_icerik,

    }
    return render(request, 'content_detail.html',context)

def product_search(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            ayar= Ayarlar.objects.get(pk=1)
            categori= Categori.objects.filter(tip = "categori")
            menu = Categori.objects.filter(tip = "menu")
            menu_icerik = Urun.objects.filter(tip = "menu")
            query=form.cleaned_data['query']
            product=(Urun.objects.filter(detail__icontains=query)|Urun.objects.filter(title__icontains=query))

            context={
                'products':product,
                'categori':categori,
                'ayar':ayar,
                'aratilan_kelime':query,
                'menu':menu,
                'menu_icerik':menu_icerik,

            }
            return render(request,'product_search.html',context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():

        q = request.GET.get('term', '')
        product = Urun.objects.filter(title__icontains=q)
        results = []
        for pl in product:

            product_json = {}
            product_json = pl.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def login_view(request):
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['masa']=random.randint(1,20)
            return HttpResponseRedirect("/")
        else:
        # Return an 'invalid login' error message.
            messages.warning(request,"Kullanıcı adı ve ya şifre yanlış!")
            return HttpResponseRedirect('/login')

    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
        'ayar':ayar,
        'categori':categori,
        'menu':menu,
        'menu_icerik':menu_icerik,
    }
    return render(request, 'login.html',context)


def join_view(request):
    if request.method=='POST':
        form=Signupform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image='images/users/bos.png'
            data.save()
            request.session['masa']=random.randint(1,20)
            return HttpResponseRedirect("/")
        else:
            messages.warning(request,"Kayıt Başarısız. Lütfen alanları kontrol ederek giriniz.")
            return HttpResponseRedirect('/join')


    form =Signupform()
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
        'ayar':ayar,
        'categori':categori,
        'form':form,
        'menu':menu,
        'menu_icerik':menu_icerik,
    }
    return render(request, 'join.html',context)


def faq(request):
    faq=FAQ.objects.all().order_by('-ordernumber')
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    context={
        'faq':faq,
        'ayar':ayar,
        'categori':categori,
        'menu':menu,
        'menu_icerik':menu_icerik,
    }
    return render(request, 'Faq.html',context)