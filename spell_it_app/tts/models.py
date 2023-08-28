from django.db import models
from celery_app import generate_collection

class Word(models.Model):

    text = models.CharField(max_length=100)
    count_frequency = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.text


class Sentence(models.Model):

    text = models.CharField(max_length=1000)
    text_decontracted = models.CharField(max_length=3000)
    text_decontracted_no_punc = models.CharField(max_length=3000)

    complexity = models.BigIntegerField(default=50)
    contained_words = models.ManyToManyField(Word)

    audio = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"(complexity: {self.complexity}) {self.text}"

class SentenceCollection(models.Model):

    name = models.CharField(max_length=50, default="Unnamed")
    sentences = models.ManyToManyField(Sentence)
    complexity_score = models.BigIntegerField(default=50)
