from django.db import models


# Create your models here.
class Album(models.Model):
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    album_title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    album_rating = models.IntegerField(choices=Rating.choices)

    def __str__(self):
        return self.title + ' - ' + self.description

class Song(models.Model):
    class Rating(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    song_rating = models.IntegerField(choices=Rating.choices)
    genre = models.CharField(max_length=20)

    def __str__(self):
        return self.song_title