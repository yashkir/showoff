from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from .models import Collection, Item, Comment, Picture
from .forms import CommentForm, PictureForm


class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['name', 'visibility']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = ['name', 'visibility']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CollectionDelete(LoginRequiredMixin, DeleteView):
    model = Collection

    def get_success_url(self):
        return reverse('collections_index')

# class ItemDetail(DetailView):
    # model = Item

class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture_form'] = PictureForm()
        return context

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item

    def get_success_url(self):
        return reverse('collections_detail', kwargs={ 'collection_id': self.object.collection.id })

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.item = Item.objects.get(id=self.kwargs['item_id'])
        return super().form_valid(form)

class PictureCreate(LoginRequiredMixin, CreateView):
    model = Picture
    form_class = PictureForm

    def form_valid(self, form):
        form.instance.item = Item.objects.get(id=self.kwargs['item_id'])
        return super().form_valid(form)

class PictureDelete(LoginRequiredMixin, DeleteView):
    model = Picture

    def get_success_url(self):
        return reverse('items_detail', kwargs={ 'pk': self.object.item.id })


def home(request):
    return render(request, 'home.html')

def collections_index(request):
    '''Only show collections visible to 'E'veryone'''
    collections = Collection.objects.filter(visibility='E')
    return render(request, 'collections/index.html', { 'collections': collections })

@login_required
def collections_index_current_user(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_index_by_user(request, user_id):
    collections = Collection.objects.filter(visibility='E', user=user_id)
    return render(request, 'collections/index.html', { 'collections': collections })

#TODO check permissions
def collections_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    return render(request, 'collections/detail.html', {
        'collection': collection,
        'items': collection.item_set.all(),
    })

#TODO check permissions
def items_detail(request, pk):
    item = Item.objects.get(id=pk)
    comment_form = CommentForm()
    print(comment_form)
    return render(request, 'main_app/item_detail.html', {
        'item': item,
        'pictures': item.picture_set.all(),
        'comments': item.comment_set.all(),
        'comment_form': comment_form,
    })


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url ='/collections/mine'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, form.instance)
        return redirect(SignUp.success_url)
