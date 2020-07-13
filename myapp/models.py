from django.db import models

class indexTable (models.Model):
    regionID = models.IntegerField(default=0, primary_key=True)
    regionName = models.CharField(max_length=200)
    regionState = models.CharField(max_length=200)
    def __str__(self):
        return self.regionID

class testState (models.Model):
    testlist = models.IntegerField(default=0)





