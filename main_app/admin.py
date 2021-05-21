from django.contrib import admin

from .models import Collection, Item, Picture, PictureS3, Comment


admin.site.register(Collection)
admin.site.register(Item)
admin.site.register(Picture)
admin.site.register(PictureS3)
admin.site.register(Comment)
