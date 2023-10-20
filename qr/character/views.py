from django.shortcuts import render

# Create your views here.



def character(request):
    return render(request, 'character/character.html')