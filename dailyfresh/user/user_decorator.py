#coding = utf-8

from django.http import HttpResponseRedirect



def log(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('is_login',None):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun