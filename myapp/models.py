from django.db import models


class StateInfo(models.Model):
    state_name = models.CharField(max_length=200)
    state_abbrev = models.CharField(max_length=200)
    def __str__(self):
        return self.state_name

class Price(models.Model):
    state = models.ForeignKey(StateInfo, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    latest_date = models.DateTimeField('date correspond to price')
    def __str__(self):
        return self.price
