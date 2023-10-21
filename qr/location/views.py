from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Location

from location.forms import LocationForm

# Create your views here.

def location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'location/location.html')


def createLocation(request):

    form = LocationForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('adminView')
    
    context = {'form': form}
    return render(request, 'location/createLocation.html', context)
    
