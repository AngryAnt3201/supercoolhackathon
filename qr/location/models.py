from django.db import models

# Create your models here.

class Location(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', default='images/placeholder.jpg', blank=True)

    def __str__(self):
        return self.name