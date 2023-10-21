from django.urls import path 
from . import views


urlpatterns = [
    path('character/<int:pk>', views.character, name='character'),
    path('createCharacter', views.createCharacter, name='createCharacter'),
    path('generateDialogue', views.generateDialogue, name='generateDialogue')
]