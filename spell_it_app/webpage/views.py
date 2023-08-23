from django.shortcuts import render
import random
from tts.models import Sentence, SentenceCollection
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from celery_app import generate_collection

def index(request):
    
    # TODO: Optimize?
    available_colllections = SentenceCollection.objects.all()
    collection_count = len(available_colllections)
    random_collection = available_colllections[random.randint(0,collection_count-1)]

    available_sentences = random_collection.sentences.all()
    sentence_count = len(available_sentences)
    random_sentence = available_sentences[random.randint(0,sentence_count-1)]


    context = {
        "collection_name": random_collection.pk,
        "random_sentence": random_sentence
    }

    return render(request=request, template_name="webpage/index.html", context=context)

def result(request, sentence_id):
    
    correct_answer = Sentence.objects.get(pk=sentence_id).text
    user_answer = request.POST["answer"]

    if  user_answer == correct_answer:
        submit_context = {
            "result_text": "Correct!",
        }
    else:
        submit_context = {
            "result_text": "Incorrect",
            "correct_answer": correct_answer,
            "user_answer": user_answer,
        }

    return render(request=request, 
                  template_name="webpage/result.html", 
                  context=submit_context)


def upload_collection(request):
    return render(request=request, template_name="webpage/upload_collection.html")

def submit_collection(request):

    generate_collection.delay(request.POST["sentences"])

    return HttpResponseRedirect(reverse("webpage:index"))