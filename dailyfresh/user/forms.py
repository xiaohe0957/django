from django import forms
from captcha.fields import CaptchaField
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput,label="用户名",max_length=128)
    password = forms.CharField(widget=forms.PasswordInput,label="密码",max_length=256)
    password1 = forms.CharField(widget=forms.PasswordInput,label="确认密码",max_length=256)
    email = forms.EmailField(widget=forms.EmailInput,label="邮箱",)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'name_input','placeholder':'请输入用户名'}), label="用户名", max_length=128)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'pass_input','placeholder':'请输入密码'}), label="密码", max_length=256)
    captcha = CaptchaField(label="验证码")

class AttrForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput,label="用户名",max_length=128)
    attrname = forms.CharField(widget=forms.TextInput, label="地址", max_length=128)
    attrphone = forms.CharField(widget=forms.TextInput,label="联系方式",max_length=11)
# (attrs={'class':'form_group'})