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
    print("IS_CELERY_WORKER")
    #from bark import preload_models
    #preload_models(text_use_small=True, coarse_use_small=True, fine_use_small=True)

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
        Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
        But I also have other interests such as playing tic tac toe.
    """
    audio_array = generate_audio(text_prompt)

    # save audio to disk
    write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)