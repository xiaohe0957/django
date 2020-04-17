from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods_Info',on_delete=models.CASCADE)
    num = models.IntegerField(null=True)