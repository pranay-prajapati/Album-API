from rest_framework import serializers
from .models import Album, Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'title', 'duration', 'rating', 'genre'
        ]


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = [
            'title', 'description', 'year', 'rating', 'songs'
        ]
