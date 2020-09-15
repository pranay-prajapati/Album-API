from rest_framework import serializers
from .models import Album, Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'song_title', 'duration', 'song_rating', 'genre'
        ]


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = [
            'album_title', 'description', 'year', 'album_rating', 'songs'
        ]
