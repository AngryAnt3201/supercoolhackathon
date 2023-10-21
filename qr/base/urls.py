from django.urls import path 
from . import views

urlpatterns = [
    path('user', views.user, name='user'),
    path('', views.index, name='index'),
    path('adminView', views.adminView, name='adminView'),
]