from django.shortcuts import render

# Create your views here.




def user(request):

    return render(request, 'base/user.html')





def index(request):

    return render(request, 'base/index.html')