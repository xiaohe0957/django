from django.urls import path
from . import views
urlpatterns = [
    path('', views.login),
    path('login/', views.login),
    path('register_exist/', views.register_exist),
    path('logout/', views.logout),
    path('userinfo/',views.user_info),
    path('addr/', views.addr),


]