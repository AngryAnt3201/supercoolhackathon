from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F
from django.http import HttpResponseRedirect, JsonResponse

import json

from .models import Character

from character.forms import CharacterForm

#Character web views

def character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, 'character/character.html', {'character': character})


def createCharacter(request):

    form = CharacterForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('adminView')

    context = {'form': form}
    return render(request, 'character/createCharacter.html', context)


def generateDialogue(request):
    print("YESSSS")

    if request.method == 'POST':
        # Parse the body of the request as JSON
        data = json.loads(request.body)
        
        # Extract the message and character from the JSON
        message = data.get('message')
        print(message)
        return_message = "fuck off"

    return JsonResponse({'status': 'success', 'message': return_message})

    