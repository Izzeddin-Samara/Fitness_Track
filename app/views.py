from django.shortcuts import render
from . import models

def index(request):
    all_the_coaches = models.show_all_coaches(request)
    return render(request, 'home.html', {'all_the_coaches': all_the_coaches})
