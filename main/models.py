from django.db import models

# Create your models here.
class Parks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(default='NewtonHills.jpg')
    