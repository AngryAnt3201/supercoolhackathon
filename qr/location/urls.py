from django.urls import path 
from . import views 

urlpatterns = [
    path('location/<int:pk>', views.location, name='location'),
    path('createLocation', views.createLocation, name='createLocation')
]