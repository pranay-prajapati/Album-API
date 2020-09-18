from rest_framework import serializers
from rest_framework.fields import empty
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from .models import Album, Song, AppBaseModel


class AppBaseSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        """

        :rtype: object
        """
        super().__init__(instance, data, **kwargs)
        # read_only_fields: list = getattr(self.Meta, 'fields', None)
        exclude: list = getattr(self.Meta, 'exclude', None)
        fields: list = getattr(self.Meta, 'fields', None)
        # exclude AppBaseModel fields
        base_fields = [f.name for f in AppBaseModel._meta.fields]
        if exclude:
            for x in base_fields:
                exclude.append(x)
            exclude = list(dict.fromkeys(exclude))
        elif not fields:
            exclude = list(dict.fromkeys(base_fields))
        self.Meta.exclude = exclude

    def get_user(self):
        """
        We can define this in a serializer and inherit that serializer.
        :return: User object
        """
        user = self.context.get("request").user
        if isinstance(user, AnonymousUser):
            return None
        return user

    @staticmethod
    def nested_create(data, serializer, **kwargs):
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save(**kwargs)

    @staticmethod
    def many_nested_create(data, serializer, **kwargs):
        serializer = serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save(**kwargs)

    @staticmethod
    def nested_update(data, instance, serializer, **kwargs):
        serializer = serializer(data=data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save(**kwargs)

    @staticmethod
    def create_many_to_many(model, data: dict, parent_value):
        """
        We're using a queryset here and not serializer as data is already validated by the parent serializer.
        Also when you try to call 'is_valid' on a serializer it throws an error that it requires a pk value.
        If we supply value, the object won't get created as django create query is run in the background and
        it requires instance and not pk value.

        @rtype: Model
        """
        model.objects.create(related=parent_value, **data)

    def get_request(self):
        return self.context.get('request')

    @property
    def _request(self):
        return self.get_request()

    def nested_update_data(self, instance, serializer, data):
        if data:
            if not instance:
                return self.nested_create(data, serializer)
            elif data:
                serializer = serializer(instance, data=data, partial=self.partial, context=self.context)
                serializer.is_valid(raise_exception=True)
                return serializer.save()

    def multiple_nested_update(self, item, serializer, model, key='id', **kwargs):
        if key in item.keys():
            instance = model.objects.get(id=item.get(key))
            return self.nested_update(item, instance, serializer, **kwargs)
        else:
            return self.nested_create(item, serializer, **kwargs)

    def multiple_nested_update_api(self, item, serializer, model, key='id', **kwargs):
        if key in item.keys():
            try:
                instance = model.objects.get(provider_id=item.get(key))
                return self.nested_update(item, instance, serializer, **kwargs)
            except ObjectDoesNotExist as e:
                print(e)
                return self.nested_create(item, serializer, **kwargs)
        else:
            return self.nested_create(item, serializer, **kwargs)

    def get_raw(self, key):
        return self.initial_data.pop(key, None)


class SongSerializer(AppBaseSerializer):
    id = serializers.IntegerField(required=False)
    album = serializers.HiddenField(default=None)

    class Meta:
        model = Song


class AlbumSerializer(AppBaseSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Album

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        album = super().create(validated_data)
        for song_data in songs_data:
            self.nested_create(song_data, SongSerializer, album=album)
        return album

    # def update(self, instance, validated_data):
    #     songs_data = validated_data.pop('songs')
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()
    #     keep_songs = []
    #     #song_data: album
    #     for song_data in songs_data:
    #         if "id" in song_data.keys():
    #             if Song.objects.filter(id=song_data['id']).exists():
    #                 s = Song.objects.get(id=song_data['id'])
    #                 s.title = song_data.get('title', s.title)
    #                 s.save()
    #                 keep_songs.append(s.id)
    #             else:
    #                 continue
    #         else:
    #             s = Song.objects.create(**song_data, album=instance)
    #             keep_songs.append(s.id)
    #
    #     for song_data in instance.songs_data:
    #         if song_data.id not in keep_songs:
    #             song_data.delete()
    #
    #     return instance
