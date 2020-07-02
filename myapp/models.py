from django.db import models

class indexTable (models.Model):
    regionID = models.IntegerField(default=0)
    regionName = models.CharField(max_length=200)
    regionState = models.CharField(max_length=200)





