from django.db import models

class indexTable (models.Model):
    regionID = models.IntegerField(default=0, primary_key=True)
    regionName = models.CharField(max_length=200)
    regionState = models.CharField(max_length=100)
    def __str__(self):
        return self.regionID

class userInformation (models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()





