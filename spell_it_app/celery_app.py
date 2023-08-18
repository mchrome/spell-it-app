import os
import time
import io
from celery import Celery
from django.conf import settings
from django.core.files import File

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
def update_tts_audio(pk):
    from tts.models import Word

    word = Word.objects.get(pk=pk)
    c, c_length, phoneme = nix.tokenize(word.text)
    xw = nix.vocalize(c, c_length)

    save_dir_path = os.path.join("tts_audio/words/",str(word.pk))
    os.makedirs(os.path.join("media",save_dir_path))
    write_wav(os.path.join("media",save_dir_path, "nix_generated.wav"), 22050, xw)

    
    word.audio_is_generated = True
    word.audio.name = os.path.join(save_dir_path, "nix_generated.wav")
    word.save(skip_audio_check=True)

    
    