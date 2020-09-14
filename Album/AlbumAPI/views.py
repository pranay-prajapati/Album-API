from django.shortcuts import render
from rest_framework import viewsets
from .models import Album #Song
from .serializers import AlbumSerializer #SongSerializer


# Create your views here.
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


# class SongViewSet(viewsets.ModelViewSet):
#     queryset = Song.objects.all()
#     serializer_class = SongSerializer
