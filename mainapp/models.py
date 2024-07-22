# Create your models here.
from django.db import models


class SteamGame(models.Model):
    appid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    detailed_description = models.TextField()
    genre = models.CharField(max_length=255)
    recommendation_count = models.IntegerField()

    def __str__(self):
        return self.name
