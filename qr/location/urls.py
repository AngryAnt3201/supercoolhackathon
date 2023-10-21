from django.urls import path 
from . import views 

urlpatterns = [
    path('location/<int:pk>', views.location, name='location'),
    path('createLocation', views.createLocation, name='createLocation'),
    path('location/<int:pk>/success', views.confirm_staff_quest, name='confirm_quest'),
]