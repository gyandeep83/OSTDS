from django.db import models

# Create your models here.
from django.db import models

class CovidCase(models.Model):
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cases = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.location} - {self.cases} cases"
