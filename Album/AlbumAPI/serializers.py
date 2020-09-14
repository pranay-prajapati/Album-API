from rest_framework import serializers
from .models import Album


class AlbumSerializer(serializers.ModelSerializer):
    songs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='song_title'
     )
    class Meta:
        model = Album
        fields = '__all__'


# class SongSerializer(serializers.ModelSerializer):
#     album_str = serializers.CharField(source='get_album_display', read_only=True)
#     class Meta:
#         model = Song
#         fields = '__all__'
