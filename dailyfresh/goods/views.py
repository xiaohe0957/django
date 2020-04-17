from django.shortcuts import render,redirect
from .models import Goods_Type,Goods_Info
from django.core.paginator import Paginator
from user import user_decorator

from cart.models import CartInfo


import json


# Create your views here.

def index(request):
    title = '首页'
    guest_cart = '1'
    type_list = Goods_Type.objects.all()
    # 新鲜水果按时间倒序排
    type0 = type_list[0].goods_info_set.order_by('-id')[0:4]
    # 新鲜水果按价格倒序排
    type01 = type_list[0].goods_info_set.order_by('-goods_price')[0:4]
    # 海鲜水产按时间倒序排
    type1 = type_list[1].goods_info_set.order_by('-id')[0:4]
    # 海鲜水产按价格倒序排
    type11 = type_list[1].goods_info_set.order_by('-goods_price')[0:4]
    # 猪牛羊肉按时间倒序排
    type2 = type_list[2].goods_info_set.order_by('-id')[0:4]
    # 猪牛羊肉按价格倒序排
    type21 = type_list[2].goods_info_set.order_by('-goods_price')[0:4]
    # 禽类蛋品按时间倒序排
    type3 = type_list[3].goods_info_set.order_by('-id')[0:4]
    # 禽类蛋品按价格倒序排
    type31 = type_list[3].goods_info_set.order_by('-goods_price')[0:4]
    # 新鲜蔬菜按时间倒序排
    type4 = type_list[4].goods_info_set.order_by('-id')[0:4]
    # 新鲜蔬菜按价格倒序排
    type41 = type_list[4].goods_info_set.order_by('-goods_price')[0:4]
    # 速冻食品按时间倒序排
    type5 = type_list[5].goods_info_set.order_by('-id')[0:4]
    # 速冻食品按价格倒序排
    type51 = type_list[5].goods_info_set.order_by('-goods_price')[0:4]
    if request.session.get('id',None):
        uid =request.session.get('id')
        carts = CartInfo.objects.filter(user_id=uid)
    else:
        return redirect('/user/login/')
    return render(request, 'index.html', locals())

@user_decorator.log
def list(request,pid,pindex,sort):
    guest_cart = '1'
    title = '商品列表'
    typeinfo = Goods_Type.objects.get(pk=int(pid)+1)
    news = typeinfo.goods_info_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list = typeinfo.goods_info_set.order_by('-id')
    elif sort == '2':
        goods_list = typeinfo.goods_info_set.order_by('goods_price')
    else:
        goods_list = typeinfo.goods_info_set.order_by('-goods_click')
    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(pindex))
    print(page.count)
    return render(request, 'list.html', locals())

# @user_decorator.log
def detail(request,id):
    title = "商品详情"
    guest_cart = '1'
    goods = Goods_Info.objects.get(pk=int(id))
    s = goods.goods_type_id-1
    goods.goods_click = goods.goods_click+1
    goods.save()
    new = goods.goods_type.goods_info_set.all().order_by('-id')[0:2]
    res = render(request, 'detail.html',locals())
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1 .remove(goods_id)
        goods_ids1.insert(0,goods_id)
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    res.set_cookie('goods_ids', goods_ids)
    return res


