from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from order.models import ShopCartForm
from order.models import ShopCart,Order,OrderProduct
from django.contrib.auth.decorators import login_required
from home.models import Ayarlar
from menu.models import Categori,Urun

# Create your views here.
def index(request):
    
    return HttpResponse("Order Page")
    
    
@login_required(login_url='/login')
def addurun(request,id):
    url=request.META.get("HTTP_REFERER")
    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            current_user=request.user
            if(ShopCart.objects.filter(urun_id=id)):
                data=ShopCart.objects.get(urun_id=id)
                data.quantity+=form.cleaned_data['quantity']
                data.save()
            else:
                data=ShopCart()
                data.user_id=current_user.id
                data.urun_id=id
                data.quantity=form.cleaned_data['quantity']
                data.save()
            request.session['cart_item']=ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request,"Siparişiniz başarıyla eklendi.")
            return HttpResponseRedirect(url)
    
    if id:
        current_user=request.user
        if(ShopCart.objects.filter(urun_id=id)):
            data=ShopCart.objects.get(urun_id=id)
            data.quantity+=1
            data.save()
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.urun_id=id
            data.quantity=1
            data.save()
        request.session['cart_item']=ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Siparişiniz başarıyla eklendi.")
        return HttpResponseRedirect(url)

    else:
        messages.warning(request,"Siparişiniz gönderilemedi. Lütfen tekrar deneyiniz belirtiniz.")
        return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    curent_user=request.user
    schopcart=ShopCart.objects.filter(user_id=curent_user.id)
    total=0;
    for rs in schopcart:
        total+=rs.urun.price*rs.quantity
    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")

    context={
                'ayar':ayar,
                'categori':categori,
                'menu':menu,
                'menu_icerik':menu_icerik,
                'shopcart':schopcart,
                'total':total,
                }
    request.session['cart_item']=ShopCart.objects.filter(user_id=curent_user.id).count()
    return render(request,'shopcart_product.html',context)
@login_required(login_url='/login')
def deletefromcart(request,id):
    current_user=request.user
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,'Urun sepetden silinmistir')
    request.session['cart_item']=ShopCart.objects.filter(user_id=current_user.id).count()
    return HttpResponseRedirect('/order/shopcart')

@login_required(login_url='/login')
def siparis(request):

    ayar= Ayarlar.objects.get(pk=1)
    categori= Categori.objects.filter(tip = "categori")
    menu = Categori.objects.filter(tip = "menu")
    menu_icerik = Urun.objects.filter(tip = "menu")

    current_user=request.user
    schopcart=ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in schopcart:
        total+=rs.urun.price*rs.quantity
    if request.method=='POST':
        data=Order()
        data.user_id=current_user.id
        data.masa=request.POST['masa']
        data.total=total
        data.status='New'
        data.ip=request.META.get('REMOTE_ADDR')
        data.save()

        for rs in schopcart:
            detail=OrderProduct()
            detail.order_id=data.id
            detail.urun_id=rs.urun_id
            detail.user_id=current_user.id
            detail.quantity=rs.quantity
            detail.price=rs.urun.price
            detail.amount=rs.amount
            detail.status='New'
            detail.save()
        ShopCart.objects.filter(user_id=current_user.id).delete()
        request.session['cart_item']=0
        messages.success(request,'Sifarisiniz Basariyla Alinmistir')
        context={
                'ayar':ayar,
                'categori':categori,
                'menu':menu,
                'menu_icerik':menu_icerik,
                'shopcart':schopcart,
                'total':total,
                }
        return HttpResponseRedirect('/user/orders')
    else:
        messages.warning(request,"Siparis Alinamadi")
        return HttpResponseRedirect('/order/shopcart')


