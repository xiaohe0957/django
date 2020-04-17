from django.db import models
from user.models import User
from goods.models import Goods_Info
# Create your models here.
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)
    odata = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    oIspay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    oaddress = models.CharField(max_length=100,default='')

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey(Goods_Info,on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField(null=True)