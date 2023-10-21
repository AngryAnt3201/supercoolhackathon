from django.urls import path 
from . import views

urlpatterns = [
    path('character/', views.character, name='character'),
    path('createCharacter', views.createCharacter, name='createCharacter'),
]