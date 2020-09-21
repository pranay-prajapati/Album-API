from django.contrib import admin
from .models import Album, Song, Podcast

# Register your models here.
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Podcast)
