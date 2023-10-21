from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

import qrcode 
from io import BytesIO
from PIL import Image
import os

from location.models import Location
from character.models import Character
from .models import Quest


from .core_func.generate_quest import QuestGenerator

# Create your views here.


def user(request):
    quests = Quest.objects.all()
    context = {'quests': quests}
    return render(request, 'base/user.html', context)


def index(request):
    generate_quests(request)
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

def generate_quests(request):

    characters = Character.objects.all()
    locations = Location.objects.all()

    character_dic = {character.name: character.description for character in characters}
    location_dic = {location.name: location.description for location in locations}
        
    quests = QuestGenerator(character_dic, location_dic, "The player has killed")
    test = quests.generate_quest("The player has stumbled into a bar")
    create_quest_object(test)


def create_quest_object(data):
    quest_name = data.get('name')
    quest_description = data.get('description')
    character_name = data.get('character')
    location_name = data.get('location')
    quest_xp = data.get('xp', 0)  # Assuming 0 XP if not provided.

    character = None
    location = None

    try:
        # Attempt to retrieve the character and location instances from the database, if provided.
        if character_name:
            character = Character.objects.get(name=character_name)

        if location_name:
            location = Location.objects.get(name=location_name)

        # Create a new Quest object. This object can handle character or location being None.
        quest = Quest(
            name=quest_name,
            description=quest_description,
            character=character,  # This can be None
            location=location,  # This can be None
            xp=quest_xp
        )

        # Save the new quest to the database
        quest.save()

        return quest

    except ObjectDoesNotExist as e:
        # This block will be triggered if the provided character or location name does not exist.
        print(f"An error occurred: {e}")
        # Additional handling can be added here, such as re-raising the exception or returning a specific value/error.

    except Exception as e:
        # Generic error handling for any other unexpected exceptions.
        print(f"An unexpected error occurred: {e}")
        # Additional handling as per your application's requirements.
    