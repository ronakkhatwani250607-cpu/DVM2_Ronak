from django.db import models

class MetroLine(models.Model):
    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MetroStation(models.Model):
    name = models.CharField(max_length=150)
    lines = models.ManyToManyField(MetroLine, related_name='stations')

    def __str__(self):
        return self.name