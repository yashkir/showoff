from django.contrib import admin

from .models import Collection, Item, Picture, Comment


admin.site.register(Collection)
admin.site.register(Item)
admin.site.register(Picture)
admin.site.register(Comment)
