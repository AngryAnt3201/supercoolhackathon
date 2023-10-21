from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
import qrcode 
from io import BytesIO
from PIL import Image
import os

from location.models import Location
from character.models import Character

# Create your views here.


def user(request):

    return render(request, 'base/user.html')



def index(request):

    return render(request, 'base/index.html')


#View of locations 
#View of characters 
#View of quest endpoints -> Company specific 
def adminView(request):
    locations = Location.objects.all()
    characters = Character.objects.all()

    context = {'locations': locations, 'characters': characters}

    return render(request, 'base/adminView.html', context)

def generate_location_qr_code(request, location_pk):
    # Get the Location instance
    location = get_object_or_404(Location, pk=location_pk)
    print(location)

    # Generate URL
    url = request.build_absolute_uri(f'/location/{location_pk}/')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code in memory
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the QR code as image response
    return HttpResponse(buffer, content_type='image/png')


def generate_qr_code(request, character_pk):
    # Get the Character instance
    character = get_object_or_404(Character, pk=character_pk)
    print(character)

    # Generate URL
    url = request.build_absolute_uri(f'/character/{character_pk}/')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code in memory
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the QR code as image response
    return HttpResponse(buffer, content_type='image/png')