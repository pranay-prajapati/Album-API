from django.db import models


# Create your models here.
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


class Album(BaseMedia):
    description = models.CharField(max_length=150)
    year = models.PositiveIntegerField()

    @property
    def songs(self):
        return self.songs_set.all()


class Song(BaseMedia):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)
    genre = models.CharField(max_length=20)
