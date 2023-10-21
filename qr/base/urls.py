from django.urls import path 
from . import views

urlpatterns = [
    path('user', views.user, name='user'),
    path('', views.index, name='index'),
    path('adminView', views.adminView, name='adminView'),
    path('generate_qr_code/<int:character_pk>', views.generate_qr_code, name='generate_qr_code'),
    path('generate_location_qr_code/<int:location_pk>', views.generate_location_qr_code, name='generate_location_qr_code')
]