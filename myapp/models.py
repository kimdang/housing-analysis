from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, default="Something")
    def __str__(self):
        return self.choice_text

class Price(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    home_value = models.PositiveIntegerField(default=0)
    rental_value = models.PositiveIntegerField(default=0)
    latest_date = models.DateTimeField('when data was collected')
    def __str__(self):
        return str(self.home_value)



