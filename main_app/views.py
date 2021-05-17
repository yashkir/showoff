from django.shortcuts import render

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
