from django.urls import path
from . import views
urlpatterns = [
    path('', views.cart),
    path('add/<gid>/<num>/', views.add),
    path('edit/<id>/<count>/', views.edit),
    path('delete/<cart_id>/', views.delete),
    path('check/', views.check),
]