from django.shortcuts import render,redirect
from user import user_decorator,models
from cart.models import CartInfo
from .models import OrderInfo,OrderDetailInfo
from django.db import transaction
from django.core.paginator import Paginator
from django.conf import settings
from goods.models import Goods_Info
from decimal import Decimal
from django.http import JsonResponse
import datetime
from alipay import AliPay
import time
import os
import random
# Create your views here.

@user_decorator.log
def order(request):
    # user = models.User.objects.get(id=request.session['id'])
    # get = request.GET
    # cart_ids = get.getlist('cart_id')
    # cart_ids1 = [int(item) for item in cart_ids]
    # carts = CartInfo.objects.filter(id_in = cart_ids1)
    # uid = request.session.get('id')
    # carts = CartInfo.objects.filter(user_id=uid)
    # totalprice = 0
    # for c in carts:
    #     totalprice = totalprice+float(c.count)*float(c.goods.goods_price)
    #     totalprice = float("%0.2f"%totalprice)
    #     print(totalprice)
    title= "订单"
    page_name ='1',
    uid = request.session.get('id')
    user = models.User.objects.get(id=uid)  # 获得用户对象 信息
    cartids = request.POST.getlist('cart_id')  # 获取多个 同名的参数
    carts = []  # 取出对应的所有cart对象
    if not cartids:
        return redirect('/cart/')
    num = 0
    yunfei =10
    allprice = 0
    totalprice = 0
    for cid in cartids:
        cart = CartInfo.objects.get(id=cid)
        carts.append(cart)
        totalprice = totalprice + float(cart.num) * float(cart.goods.goods_price)
        totalprice = float('%0.2f' % totalprice)
        num = num +cart.num
    allprice = totalprice+yunfei
    ca_id = ','.join(cartids)
    context = {

                'user': user,
               'carts': carts,
               'total_price': totalprice}
    return render(request, 'price_order.html', locals())


@user_decorator.log
@transaction.atomic()
def order_handle(request):
    user_id = request.session.get('id')
    user_name = request.session.get('name')
    tran_id = transaction.savepoint()
    try:
        cart_ids = request.POST.get('sku_ids')
        if not user_id:
            return JsonResponse({'res': 0,'errmsg':"用户未登录"})
        order_data =datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(user_id)
        # time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        total_count = 0
        total_price = 0
        order = OrderInfo.objects.create(
            oid=order_data,
            user=models.User.objects.get(id=user_id),
            odata=time_now,
            ototal=total_price,
        )
        cart_ids =cart_ids.split(',')
        for cart_id in cart_ids:
            try:
                cart = CartInfo.objects.get(id=cart_id)
            except:
                return JsonResponse({'res': 1,'errmsg':"商品不存在"})
            detail = OrderDetailInfo.objects.create(
                order=order,
                goods=cart.goods,
                price=cart.goods.goods_price,
                count=cart.num,
            )
            goods = cart.goods
            if goods.goods_stock < int(cart.num):
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'res': 1,'errmsg':'库存不足'})
            goods.goods_stock = goods.goods_stock-int(cart.num)
            goods.save()
            # cart.goods.goods_stock = int(cart.goods.goods_stock)-int(cart.num)
            # cart.goods.save()
            amount = cart.goods.goods_price*int(cart.num)
            total_price = total_price+amount
            total_count = total_count+int(detail.count)
            # detail.price = total_price
            # detail.count = total_count
            detail.save()
            cart.delete()
        order.ototal=total_price
        order.save()
        return JsonResponse({'res': 5,'msg':"创建成功"})
    except Exception as e:
        msg = e
        transaction.savepoint_rollback(tran_id)
        return JsonResponse({'res': 3,'msg':msg})


@user_decorator.log
def pay(request,pindex):
    # order =OrderInfo.objects.get(id=oid)
    # order.oIspay = True
    # order.save()
    page_name = '1'
    title = '用户中心订单页面'
    user_id = request.session.get('id')
    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-odata')
    for o in orders:
        goods = OrderDetailInfo.objects.filter(order_id=o.oid)
        for good in goods:
            amount = good.price*good.count
            good.amount = amount
        o.goods = goods
    paginator = Paginator(orders,3)
    page = paginator.page(pindex)

    return render(request,'user_price_order.html',locals())


def alipay(request):
    user_id = request.session.get('id')
    order_id = request.POST.get("order_id")
    if not order_id:
        return JsonResponse({'res': 1, 'errmsg': '无效的订单id'})
    try:
        order = OrderInfo.objects.get(oid=order_id,
                                      user=models.User.objects.get(id=user_id),
                                      oIspay=0)
    except OrderInfo.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '订单错误'})
    merchant_private_key_path = settings.BASE_DIR + '/order/ppPrivate_key.pem'
    alipay_public_key_path = settings.BASE_DIR + '/order/lipayPub_key.pem'
    app_private_key_string = open(merchant_private_key_path).read()
    alipay_public_key_string = open(alipay_public_key_path).read()
    # print(app_private_key_string)
    # app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    # {}-----END RSA PRIVATE KEY-----
    # """.format(app_private_key_string)
    # alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    # {}-----END PUBLIC KEY-----
    # """.format(alipay_public_key_string)
    alipay = AliPay(
        appid="2016102300747786",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        # app_private_key_path=os.path.join(settings.BASE_DIR, 'ppPrivate_key.pem'),
        # alipay_public_key_path=os.path.join(settings.BASE_DIR, 'lipayPub_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True
    )
    # order_id: 202004121112491
    # 202004121110571
    total_pay = order.ototal
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单id
        total_amount=str(total_pay),  # 支付总金额
        subject='小何。',
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return JsonResponse({'res': 3, 'pay_url': pay_url})


def check(request):
    user_id = request.session.get('id')
    order_id = request.POST.get("order_id")
    if not order_id:
        return JsonResponse({'res': 1, 'errmsg': '无效的订单id'})
    try:
        order = OrderInfo.objects.get(oid=order_id,
                                      user=models.User.objects.get(id=user_id),
                                      oIspay=0)
    except OrderInfo.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '订单错误'})
    merchant_private_key_path = settings.BASE_DIR + '/order/ppPrivate_key.pem'
    alipay_public_key_path = settings.BASE_DIR + '/order/lipayPub_key.pem'
    app_private_key_string = open(merchant_private_key_path).read()
    alipay_public_key_string = open(alipay_public_key_path).read()
    alipay = AliPay(
        appid="2016102300747786",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        # app_private_key_path=os.path.join(settings.BASE_DIR, 'ppPrivate_key.pem'),
        # alipay_public_key_path=os.path.join(settings.BASE_DIR, 'lipayPub_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True
    )
    while True:
        response = alipay.api_alipay_trade_query(order_id)

        # response = {
        #         "trade_no": "2017032121001004070200176844", # 支付宝交易号
        #         "code": "10000", # 接口调用是否成功
        #         "invoice_amount": "20.00",
        #         "open_id": "20880072506750308812798160715407",
        #         "fund_bill_list": [
        #             {
        #                 "amount": "20.00",
        #                 "fund_channel": "ALIPAYACCOUNT"
        #             }
        #         ],
        #         "buyer_logon_id": "csq***@sandbox.com",
        #         "send_pay_date": "2017-03-21 13:29:17",
        #         "receipt_amount": "20.00",
        #         "out_trade_no": "out_trade_no15",
        #         "buyer_pay_amount": "20.00",
        #         "buyer_user_id": "2088102169481075",
        #         "msg": "Success",
        #         "point_amount": "0.00",
        #         "trade_status": "TRADE_SUCCESS", # 支付结果
        #         "total_amount": "20.00"
        # }

        code = response.get('code')
        if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
            # 支付成功
            # 获取支付宝交易号
            # trade_no = response.get('trade_no')
            # # 更新订单状态
            # order.trade_no = trade_no
            order.oIspay=True
            order.save()
            # 返回结果
            return JsonResponse({'res': 3, 'message': '支付成功'})
        elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
            # 等待买家付款
            # 业务处理失败，可能一会就会成功
            import time
            time.sleep(5)
            continue
        else:
            # 支付出错
            print(code)
            return JsonResponse({'res': 4, 'errmsg': '支付失败'})