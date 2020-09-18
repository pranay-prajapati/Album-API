from rest_framework import serializers
from .models import Album, Song


class SongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Song
        fields = [
            'id', 'title', 'duration', 'rating', 'genre'
        ]
        read_only_fields = ('title',)


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'description', 'year', 'rating', 'songs'
        ]

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        for song_data in songs_data:
            Song.objects.create(album=album, **song_data)
        return album

    def update(self, instance, validated_data):
        songs_data = validated_data.pop('songs')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        keep_songs = []
        for song_data in songs_data:
            if "id" in song_data.keys():
                if Song.objects.filter(id=song_data['id']).exists():
                    s = Song.objects.get(id=song_data['id'])
                    s.title = song_data.get('title', s.title)
                    s.save()
                    keep_songs.append(s.id)
                else:
                    continue
            else:
                s = Song.objects.create(**song_data, album=instance)
                keep_songs.append(s.id)

        for song_data in instance.songs_data:
            if song_data.id not in keep_songs:
                song_data.delete()

        return instance
