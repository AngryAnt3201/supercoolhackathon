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
    location = data.get('location')  # Uncomment this if the location is provided
    # location_name = data.get('location')  # Uncomment this if the location's name is also provided in the data.
    quest_xp = data.get('xp', 0)  # Assuming 0 XP if not provided.

    try:
        # Get the character and location instances from the database.
        # It's assuming that 'character_name' and 'location_name' are the unique names of the objects.
        character = Character.objects.get(name=character_name)
        # location = Location.objects.get(name=location_name)  # Uncomment if location is provided

        # Create a new Quest object
        quest = Quest(
            name=quest_name,
            description=quest_description,
            character=character,
            location=location,  # Uncomment if location is provided
            xp=quest_xp
        )

        # Save the new quest to the database
        quest.save()

        return quest

    except ObjectDoesNotExist as e:
        # This block will be triggered if either the character or location does not exist.
        # Handle the error as appropriate for your application's needs.
        print(f"An error occurred: {e}")  # Simple print statement for demonstration; consider logging the error.
        # You might want to return something relevant here, depending on your application's logic.

    except Exception as e:
        # Generic error handling, adapt as needed
        print(f"An unexpected error occurred: {e}")  # Again, consider proper logging in a production scenario.
        # Handle the error appropriately for your application's needs.

    pass
    