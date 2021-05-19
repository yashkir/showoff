from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from .models import Collection, Item, Comment
from .forms import CommentForm


def add_user_to_form_valid(method):
    '''Add current user to the form'''
    def wrapped(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return method(self, form)
    return wrapped


class CollectionCreate(CreateView):
    model = Collection
    fields = ['name', 'visibility']

    @add_user_to_form_valid
    def form_valid(self, form):
        return super().form_valid(form)

class CollectionUpdate(UpdateView):
    model = Collection
    fields = ['name', 'visibility']

    @add_user_to_form_valid
    def form_valid(self, form):
        return super().form_valid(form)

class CollectionDelete(DeleteView):
    model = Collection

    def get_success_url(self):
        return reverse('collections_index')

# class ItemDetail(DetailView):
    # model = Item

class ItemCreate(CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(UpdateView):
    model = Item
    fields = '__all__'

class ItemDelete(DeleteView):
    model = Item

    def get_success_url(self):
        return reverse('collections_detail', kwargs={ 'collection_id': self.object.collection.id })

class CommentCreate(CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.item = Item.objects.get(id=self.kwargs['item_id'])
        return super().form_valid(form)


def home(request):
    return render(request, 'home.html')

def collections_index(request):
    '''Only show collections visible to 'E'veryone'''
    collections = Collection.objects.filter(visibility='E')
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_index_by_user(request, user_id):
    collections = Collection.objects.filter(user=user_id)
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    return render(request, 'collections/detail.html', {
        'collection': collection,
        'items': collection.item_set.all(),
    })

def items_detail(request, pk):
    item = Item.objects.get(id=pk)
    comment_form = CommentForm()
    print(comment_form)
    return render(request, 'main_app/item_detail.html', {
        'item': item,
        'comments': item.comment_set.all(),
        'comment_form': comment_form,
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
