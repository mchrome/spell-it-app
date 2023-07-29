from django.db import models

class Word(models.Model):

    text = models.CharField(max_length=100)
    count_frequency = models.BigIntegerField(default=0)


    def __str__(self):
        return self.text
    