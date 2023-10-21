from django.db import models
from qr import settings
from character.models import Character
from location.models import Location

# Create your models here.


    
class Quest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    xp = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
