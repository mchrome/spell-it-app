import os
import time
import io
from celery import Celery
from django.conf import settings
from django.core.files import File
import uuid 
from django.db import transaction

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

@app.task()
def debug_task():
    time.sleep(5)
    print('Hello form debug_task')

@app.task()
def check_cuda():
    import torch
    print('Cuda availability: ', torch.cuda.is_available())

@app.task()
def bark_tts():
    from bark import SAMPLE_RATE, generate_audio
    from scipy.io.wavfile import write as write_wav
    # generate audio from text
    text_prompt = """
        Hello Hello Hello
    """
    audio_array = generate_audio(text_prompt)

    # save audio to disk
    write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)

@app.task()
def nix_tts():
    # Tokenize input text
    c, c_length, phoneme = nix.tokenize("Born to multiply, born to gaze into night skies.")
    # Convert text to raw speech
    xw = nix.vocalize(c, c_length)
    write_wav("nix_generated.wav", 22050, xw)

@app.task()
def generate_collection(user_input: str):
    from tts.models import Sentence, SentenceCollection

    collection = SentenceCollection()
    sentence_pk_list = []
    
    for text in user_input.split("\n"):
        # Generate audio for the sentence
        c, c_length, phoneme = nix.tokenize(text)
        audio = nix.vocalize(c, c_length)
        # Save the audio
        save_dir_path = os.path.join("tts_audio/sentence/",str(uuid.uuid4()))
        os.makedirs(os.path.join("media",save_dir_path))
        write_wav(os.path.join("media",save_dir_path, "nix_generated.wav"), 22050, audio)
        # Create model instance
        # TODO: Save stripped copy of initial text
        # to compare with, when checking if user's guess is correct
        sentence = Sentence(text=text)
        sentence.audio.name = os.path.join(save_dir_path, "nix_generated.wav")
        sentence.save()
        sentence_pk_list.append(sentence.pk)
    
    print(sentence_pk_list)

    with transaction.atomic():
        collection.save()
        collection.sentences.add(*sentence_pk_list)    
        
        

    
        

    
    