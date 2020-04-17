  # coding=utf-8
from haystack import indexes
from goods.models import Goods_Info # 导入商品类

class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Goods_Info

    def index_queryset(self, using=None):
        return self.get_model().objects.all()