from django.shortcuts import render

from .models import Collection


def home(request):
    return render(request, 'home.html')

def collections_index(request):
    collections = Collection.objects.all()
    return render(request, 'collections/index.html', { 'collections': collections })
