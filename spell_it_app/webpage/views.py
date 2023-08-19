from django.shortcuts import render
import random
from tts.models import Word
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):

    available_words = Word.objects.all().filter(audio_is_generated=True)

    word_count = available_words.count()
    random_word = available_words[random.randint(0,word_count-1)]
    #random_word_pk = available_words[random_word].pk

    context = {
        "random_word": random_word
    }
    return render(request=request, template_name="webpage/index.html", context=context)

def submit(request, word_id):
    if request.POST["answer"] == Word.objects.get(pk=word_id).text:
        result_text = "Correct!"
    else:
        result_text = "Incorrect"

    return render(request=request, 
                  template_name="webpage/result.html", 
                  context={"result_text": result_text})