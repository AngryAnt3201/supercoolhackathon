from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Location

from base.models import Quest

from location.forms import LocationForm

import base64
import qrcode
from io import BytesIO
from PIL import Image
import os

import openai 

openai.api_key = os.environ.get('OPENAI_API_KEY')
# Create your views here.

def location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    quest_location = Quest.objects.filter(location=location)
    
    context = {'location': location}

    if location.staff_flagged:
        qr_code_image = generate_QR(request, pk)
        context['qr_code_image'] = qr_code_image
    else:
        
        for quest in quest_location:
            quest.completed = True
            quest.save()

        queststr = create_message(pk)
        if queststr is not None:
            context['queststr'] = queststr
        

    return render(request, 'location/location.html', context)


def confirm_staff_quest(request, pk):

    location = get_object_or_404(Location, pk=pk)
    quest_location = Quest.objects.filter(location=location)
    for quest in quest_location:
            quest.completed = True
            quest.save()
    return None

def generate_QR(request, pk):
     
     url = request.build_absolute_uri(f'/location/{pk}/success')

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
     img.save(buffer, format="PNG")
     qr_code_image = base64.b64encode(buffer.getvalue()).decode()

     return qr_code_image



def create_message(pk): 
     
    location = get_object_or_404(Location, pk=pk)
    quest_location = Quest.objects.filter(location=location)

    # List to hold quest information
    quest_info_list = []

    for quest in quest_location:
        # Using f-strings for cleaner formatting (requires Python 3.6+)
        quest_info = f"Name: {quest.name} Description: {quest.description}"
        quest_info_list.append(quest_info)

    # Join the quest information strings, separating each with a new line
    quest_str = '\n'.join(quest_info_list)
    print(quest_str)

    messages = [
          {'role': 'system', 'content': 'Based off the list of quests associated with a location, provided some lore and say the user has successfully completed the quest'}, 
          {'role': 'system', 'content': 'This is the quest: ' + str(quest_str)}
          ]
     

    response = openai.ChatCompletion.create(
            model='gpt-4-0613',
            temperature=0.1,
            messages = messages, 
            max_tokens=200,
        )

    return response['choices'][0].message['content']


def createLocation(request):

    form = LocationForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('adminView')
    
    context = {'form': form}
    return render(request, 'location/createLocation.html', context)
    
