from django.db import models


# Create your models here.
class AppBaseModel(models.Model):
    """
    The base model for every model. Make sure you inherit this while making models except User related models.
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

class BaseMedia(models.Model):
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    title = models.CharField(max_length=100)
    rating = models.IntegerField(choices=Rating.choices)

    class Meta:
        abstract = True

        def __str__(self):
            return self.title


class Album(AppBaseModel,BaseMedia):
    description = models.CharField(max_length=150)
    year = models.PositiveIntegerField()

    @property
    def songs(self):
        return self.songs_set.all()


class Song(AppBaseModel,BaseMedia):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)
    genre = models.CharField(max_length=20)
