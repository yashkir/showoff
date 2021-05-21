from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView

import os
import boto3
import uuid

from .models import Collection, Item, Comment, Picture, PictureS3
from .forms import CommentForm, PictureForm

S3_BASE_URL = os.getenv('S3_BASE_URL')
BUCKET = os.getenv('BUCKET')


class Home(TemplateView):
    template_name = 'home.html'


class CollectionList(ListView):
    model = Collection
    queryset = Collection.objects.filter(visibility='E')


class CollectionListCurrentUser(LoginRequiredMixin, ListView):
    model = Collection

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class CollectionDetail(DetailView):
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(collection=self.object)
        return context


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


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'pictures': self.object.picture_set.all(),
            'comments': self.object.comment_set.all(),
            'comment_form': CommentForm(),
        })
        return context


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
        return reverse('collections_detail', kwargs={ 'pk': self.object.collection.id })


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.item = Item.objects.get(id=self.kwargs['item_id'])
        return super().form_valid(form)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('items_detail', kwargs={ 'pk': self.object.item.id })


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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url ='/collections/mine'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, form.instance)
        return redirect(SignUp.success_url)


def add_s3_picture(request, collection_id):
    file = request.FILES.get('file', None)

    if file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + file.name[file.name.rfind('.'):]

        s3.upload_fileobj(file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        pictures3 = PictureS3(collection_id=collection_id, url=url)
        pictures3.save()

    return redirect('collections_detail', pk=collection_id)
