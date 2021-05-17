from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Collection, Item


def home(request):
    return render(request, 'home.html')

def collections_index(request):
    collections = Collection.objects.all()
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_index_by_user(request, user_id):
    collections = Collection.objects.filter(user=user_id)
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    items = Item.objects.filter(collection=collection_id)
    return render(request, 'collections/detail.html', {
        'collection': collection,
        'items': items,
    })

def items_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'items/detail.html', {
        'item': item,
    })

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        result = login(request, user)
        # TODO redirect to user's collections
        return redirect('/')
    else:
        return redirect('/')

def user_logout(request):
    logout(request)
    return redirect('/')
