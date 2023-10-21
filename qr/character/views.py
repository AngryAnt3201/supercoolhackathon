from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F
from django.http import HttpResponseRedirect, JsonResponse

from django.core.cache import cache

import json

from .models import Character

from .core_func.character_chat import Character_AI

from character.forms import CharacterForm

from base.models import Quest

#Character web views

current_character = None

def character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    quests = Quest.objects.filter(character=character)
    quest_strings = []

    for quest in quests:
        # Combine the quest name and description into a single string
        quest_string = f"{quest.name}: {quest.description}"
        quest_strings.append(quest_string)
    current_character = Character_AI(character.name, character.description, "You are in newyork during the 1930's", "These are quests associated with your character: " + str(quest_strings))

    cache_key = 'character_' + str(pk)
    cache.set(cache_key, current_character, 60 * 60 * 24)

    return render(request, 'character/character.html', {'character': character, 'cache_key': cache_key, 'quests': quests})


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
        cache_dir = data.get('cache_key')
        pk = data.get('pk')
        current_character = cache.get(cache_dir)
        
        return_message = current_character.generate_dialogue(message)

        if isinstance(return_message, tuple):

            #Complete Quest
            
            character = get_object_or_404(Character, pk=pk)
            quests = Quest.objects.filter(character=character)
            for quest in quests:
                quest.completed = True
                quest.save()


            return_message = return_message[0]

    return JsonResponse({'status': 'success', 'message': return_message})

    