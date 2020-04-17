from django.urls import path
from . import views
urlpatterns = [
    path('handle/', views.order_handle),
    path('place/', views.order),
    path('pay/<pindex>/', views.pay),
    path('alipay', views.alipay),
    path('check', views.check),


]