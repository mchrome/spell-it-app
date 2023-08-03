import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spell_it_app.settings')

app = Celery('spell_it_app')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

if os.getenv("IS_CELERY_WORKER") == "1":
    # download and load all models
    #from bark import preload_models
    #preload_models(text_use_small=True, coarse_use_small=True, fine_use_small=True)
    pass

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
    from nix.models.TTS import NixTTSInference
    from scipy.io.wavfile import write as write_wav
    # Initiate Nix-TTS
    nix = NixTTSInference(model_dir = "/tts_models/nix-ljspeech-deterministic-v0.1")
    # Tokenize input text
    c, c_length, phoneme = nix.tokenize("Born to multiply, born to gaze into night skies.")
    # Convert text to raw speech
    xw = nix.vocalize(c, c_length)
    write_wav("nix_generated.wav", 22050, xw)