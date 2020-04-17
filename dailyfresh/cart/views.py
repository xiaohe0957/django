from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core import serializers
from user import user_decorator
from . import models
# Create your views here.
# @user_decorator.log
def cart(request):
    title = '购物车'
    page_name = '1'
    uid = request.session['id']
    carts = models.CartInfo.objects.filter(user_id = uid)
    return render(request,'cart.html',locals())

# @user_decorator.log
def add(request,gid,num):
    uid = request.session['id']
    gid = gid
    carts = models.CartInfo.objects.filter(user_id=uid,goods_id = gid)
    if len(carts)>=1:
        cart = carts[0]
        if cart.num == None:
            cart.num = 0
        cart.num = cart.num+int(num)
    else:
        cart = models.CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.num = num
    cart.save()
    if request.is_ajax():
        num = serializers.serialize('json', models.CartInfo.objects.filter(user_id=request.session['id']))
        data = {
            'num': num
        }
        return JsonResponse(data)
    else:
        return redirect('/cart/')



# @user_decorator.log
def edit(request,id,count):
    try:
        cart = models.CartInfo.objects.get(pk=int(id))
        count1 = cart.num = int(count)
        cart.save()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':count1}
    return JsonResponse(data)

# @user_decorator.log
def delete(request,cart_id):
    try:
        cart =models.CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok',0}
    return JsonResponse(data)

def check(request):
    data = {'ok':1}
    return JsonResponse(data)
