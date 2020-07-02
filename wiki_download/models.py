from django.db import models

# Create your models here.

class Wiki(models.Model):
    title=models.TextField()
    url=models.URLField()

