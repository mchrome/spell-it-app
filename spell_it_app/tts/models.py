from django.db import models
from celery_app import generate_collection

class Word(models.Model):

    text = models.CharField(max_length=100)
    count_frequency = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.text


class Sentence(models.Model):

    text = models.CharField(max_length=1000)
    complexity = models.BigIntegerField(default=50)
    contained_words = models.ManyToManyField(Word)

    audio = models.FileField(blank=True, null=True)

    # def save(self, skip_audio_check=False, *args, **kwargs):
        
    #     if skip_audio_check:
    #         return super().save(*args, **kwargs)

    #     if self.pk is None or Word.objects.get(pk=self.pk).text != self.text:
    #         self.audio_is_generated = False
    #         return_value = super().save(*args, **kwargs)
    #         update_tts_audio.delay(self.pk)
    #         return return_value
    #     else:
    #         return super().save(*args, **kwargs)

    def __str__(self):
        return f"(complexity: {self.complexity}) {self.text}"

class SentenceCollection(models.Model):

    name = models.CharField(max_length=50)
    sentences = models.ManyToManyField(Sentence)
    complexity_score = models.BigIntegerField(default=50)
