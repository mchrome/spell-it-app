import os
import time
import io
from celery import Celery
from django.conf import settings
from django.core.files import File
import uuid 
from django.db import transaction
from django.db.models import Sum
import string
from django.db.models import Sum, F
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from math import ceil
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spell_it_app.settings')

app = Celery('spell_it_app')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

if os.getenv("IS_CELERY_WORKER") == "1":
    from nix.models.TTS import NixTTSInference
    from scipy.io.wavfile import write as write_wav
    # Initiate Nix-TTS
    nix = NixTTSInference(model_dir = "/tts_models/nix-ljspeech-deterministic-v0.1")


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

@app.task()
def generate_collection(user_input: str):
    from tts.models import Sentence, SentenceCollection, Word

    collection = SentenceCollection()
    sentence_pk_list = []
    
    complexity_sum = 0
    collection_word_count = 0

    total_cnt_words = Word.objects.count()    

    for text in user_input.split("\n"):
        
        if len(text) == 0:
            continue

        text_dec = decontracted(text)

        # Add up frequencies of words in a sentence
        no_punctuation_sentence = text_dec.translate(str.maketrans('', '', string.punctuation))
        split_sentence = no_punctuation_sentence.split()
        sentence_complexity = 0
        for word in split_sentence:

            word_obj = Word.objects.filter(text=word).annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F('count_frequency').asc()
                ),
            ).first()

            if word_obj:
                sentence_complexity += word_obj.rank
            else:
                sentence_complexity +=  ceil(0.2 * total_cnt_words)
        
        complexity_sum += sentence_complexity
        collection_word_count += len(split_sentence)

        sentence_complexity = 100 - int(sentence_complexity/total_cnt_words/len(split_sentence)*100)

        # Generate audio for the sentence
        c, c_length, phoneme = nix.tokenize(text_dec)
        audio = nix.vocalize(c, c_length)

        # Save the audio
        save_dir_path = os.path.join("tts_audio/sentence/",str(uuid.uuid4()))
        os.makedirs(os.path.join("media",save_dir_path))
        write_wav(os.path.join("media",save_dir_path, "nix_generated.wav"), 22050, audio)
        
        # Create model instance
        # TODO: Save stripped copy of initial text
        # to compare with, when checking if user's guess is correct
        sentence = Sentence()
        sentence.text = text
        sentence.text_decontracted = text_dec
        sentence.text_decontracted_no_punc = no_punctuation_sentence
        sentence.audio.name = os.path.join(save_dir_path, "nix_generated.wav")
        sentence.complexity = sentence_complexity
        sentence.save()
        sentence_pk_list.append(sentence.pk)
    
    print(sentence_pk_list)

    with transaction.atomic():
        collection.complexity_score = 100 - int(complexity_sum/total_cnt_words/collection_word_count*100)
        collection.save()
        collection.sentences.add(*sentence_pk_list)    
        
        

    
        

    
    