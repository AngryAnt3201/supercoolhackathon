from django.shortcuts import render, redirect
from django.db.models import Q, F

from character.forms import CharacterForm

#Character web views


def character(request):
    return render(request, 'character/character.html')


def createCharacter(request):

    form = CharacterForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return redirect('adminView')

    context = {'form': form}
    return render(request, 'character/createCharacter.html', context)