from django.db import models


# Create your models here.
class Goods_Type(models.Model):
    goods_title = models.CharField(max_length=20)
    is_Delete = models.BooleanField(default=False)

    def __str__(self):
        return self.goods_title

class Goods_Info(models.Model):
    goods_name = models.CharField(max_length=20)
    goods_image = models.ImageField(upload_to='goods')
    goods_price = models.DecimalField(max_digits=5,decimal_places=2)
    is_Delete = models.BooleanField(default=False)
    goods_click = models.IntegerField()
    goods_unit = models.CharField(max_length=20,default='500g')
    goods_introduce = models.CharField(max_length=200)
    goods_stock = models.IntegerField()
    goods_content = models.CharField(max_length=1000)
    goods_type = models.ForeignKey(Goods_Type,on_delete=models.CASCADE)

    def __str__(self):
        return self.goods_name

