from django.contrib import admin
from .models import Goods_Type,Goods_Info

# Register your models here.
class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods_title']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'goods_name', 'goods_price', 'goods_unit', 'goods_introduce', 'goods_stock', 'goods_content']

admin.site.register(Goods_Type,GoodsTypeAdmin)
admin.site.register(Goods_Info,GoodsInfoAdmin)