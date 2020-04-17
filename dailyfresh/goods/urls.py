from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('<pid>/<pindex>/<sort>/', views.list),
    path('<id>/', views.detail)
]