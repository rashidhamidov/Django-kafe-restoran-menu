from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from menu.models import Categori,Comment
from home.models import Ayarlar,UserProfile
from order.models import Order,OrderProduct
from user.forms import UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from menu.models import Urun, Images, ImageFormContent


@login_required(login_url='/login')
def index(request):
    if request.user is not None:
        current_user=request.user
        profile=UserProfile.objects.get(user_id=current_user.id)
        ayar= Ayarlar.objects.get(pk=1)
        categori= Categori.objects.filter(tip = "categori")
        menu = Categori.objects.filter(tip = "menu")
        menu_icerik = Urun.objects.filter(tip = "menu")
        context={
            'ayar':ayar,
            'categori':categori,
            'profile':profile,
            'menu':menu,
            'menu_icerik':menu_icerik,
            }
        return render(request, 'user.html',context)
    else:
        return redirect('/login')

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profiliniz Guncellendi")
            return redirect('/user')

    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.userprofile)
        categori= Categori.objects.filter(tip = "categori")
        menu = Categori.objects.filter(tip = "menu")
        menu_icerik = Urun.objects.filter(tip = "menu")
        ayar= Ayarlar.objects.get(pk=1)
        context={
            'ayar':ayar,
            'categori':categori,
            'user_form':user_form,
            'profile_form':profile_form,
            'menu':menu,
            'menu_icerik':menu_icerik,
        }
        return render(request,'bilgi_yenile.html',context)

 
@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user) # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirildi')
            return redirect('/user')
        else:
            messages.warning(request, 'Lütfen hatalara dikkat ediniz.<br>'+str(form.errors))

    
    ayar=Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    form = PasswordChangeForm(request.user)
    context={
            'ayar':ayar,
            'categori':categori,
            'form':form,
            'menu':menu,
            'menu_icerik':menu_icerik,
        }
    return render(request, 'sifre_yenile.html',context)

@login_required(login_url='/login') # Check togin
def comments (request):
    ayar=Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'ayar':ayar,
        'categori': categori,
        'comments': comments,
        'menu':menu,
        'menu_icerik':menu_icerik,
      }
    return render(request, 'user_comment.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    Comment.objects.filter(id=id).delete()
    messages.warning(request,"Yorumunuz  silinmiştir.")
    return HttpResponseRedirect("/user/comments")




@login_required(login_url='/login')
def orders(request):
    ayar=Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id).order_by('-update_at')
    context = {
        'ayar':ayar,
        'categori': categori,
        'orders': orders,
        'menu':menu,
        'menu_icerik':menu_icerik,
      }
    return render(request, 'user_order.html', context)
@login_required(login_url='/login')
def orderdetail(request,id):
    current_user = request.user
    orders=OrderProduct.objects.filter(order_id=id)
    context = {
        'orders': orders
      }
    return render(request,'orderdetail.html',context)
