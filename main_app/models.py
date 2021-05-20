from django.shortcuts import reverse
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

VISIBILITIES = (
    ('P', 'Private'),
    ('F', 'Friends'),
    ('E', 'Everyone'),
)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    visibility = models.CharField(max_length=1, choices=VISIBILITIES, default=VISIBILITIES[0][0])

    def __str__(self):
        return f"{self.name} ({self.get_visibility_display()})"

    def get_absolute_url(self):
        return reverse('collections_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name']


class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['name']


class Picture(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    image = models.ImageField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={'pk': self.item.id})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(1024)

    def __str__(self):
        return self.text[:64]

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={'pk': self.item.id})
