from django.shortcuts import reverse
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    is_public = models.BooleanField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collections_detail', kwargs={'collection_id': self.id})


class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={'pk': self.id})


class Picture(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(1024)

    def __str__(self):
        return self.text[:64]
