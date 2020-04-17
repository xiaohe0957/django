from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from . import forms

from user import user_decorator

from .models import User
from goods.models import Goods_Info


# Create your views here.

def register(request):
    title = '注册'
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = '请检查输入内容'

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            password1 = register_form.cleaned_data.get('password1')
            email = register_form.cleaned_data.get('email')
            if password != password1:
                message = "两次密码不一致"
                return render(request, "register.html",locals())
            else:
                same_user_name = User.objects.filter(username=username)
                if same_user_name:
                    message = "用户名已存在啦"
                    return render(request,'register.html',locals())

            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            return redirect('/user/login/')
    register_form = forms.RegisterForm()
    return render(request, 'register.html',locals())

#注册页AJAX验证用户名
def register_exist(request):
    username = request.GET.get('username')
    count = User.objects.filter(username=username).count()
    return JsonResponse({'count': count})


def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    title = '登录'
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        message = "请检查填写的内容"

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                message = "用户名不存在"
                return render(request,"login.html",locals())
            if user.password == password:
                url = request.COOKIES.get('url', '/index/')
                red = HttpResponseRedirect(url)
                request.session['is_login'] = True
                request.session['name'] = username
                request.session['id'] = user.id
                return red
            else:
                message = '密码错误'
                return render(request,'login.html',locals())
        else:
            return render(request,'login.html',locals())
    login_form = forms.LoginForm()
    return render(request,'login.html',locals())



def logout(request):
    request.session.flush()
    return redirect('/index/')


@user_decorator.log
def user_info(request):
    page_name = '1'
    title = '用户中心'
    user_email = User.objects.get(id = request.session['id']).email
    username = User.objects.get(id=request.session['id']).username
    user_phone = User.objects.get(id=request.session['id']).phone
    user_addr = User.objects.get(id=request.session['id']).address
    goods_ids = request.COOKIES.get('goods_ids','')
    # goods_ids1 = goods_ids.split(',')
    # goods_list = []
    # for goods_id in goods_ids1:
    #     try:
    #         goods_list.append(Goods_Info.objects.get(id = int(goods_id)))
    #     except:
    #         goods_list.append(Goods_Info.objects.get(id=2))
    if goods_ids != '':

        goodidsl = goods_ids.split(',')  # 拆分为列表

        # 这样查询可以的到所需商品，但顺序无法维护，无法为原先设定顺序

        # GoodInfo.objects.filter(id__in=goodids)

        goods_list = []  # 用来存放 商品列表，并维持顺序不变

        for good_id in goodidsl:
            goods = Goods_Info.objects.filter(pk=good_id).first()

            goods_list.append(goods)



    else:

        goods_list = []

    context = {'title': '用户中心', 'username': username, 'phone': user_phone, 'adress': user_addr,



    'good_list': goods_list, 'tag': 1}
    return render(request,'user_center_info.html',locals())

def addr(request):
    page_name = '1'
    title = '用户中心信息更新'
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        attr_form = forms.AttrForm(request.POST)
        message = '请检查输入内容'
        if attr_form.is_valid():
            username = attr_form.cleaned_data.get('username')
            attrname = attr_form.cleaned_data.get('attrname')
            phone = attr_form.cleaned_data.get('attrphone')
            user.username = username
            user.address = attrname
            user.phone = phone
            user.save()
            return redirect('/user/userinfo/')
        return render(request,'user_info_addr.html',locals())
    attr_form = forms.AttrForm()
    return render(request,'user_info_addr.html',locals())