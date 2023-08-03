from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        "audio_path": "bark_out.wav"
    }
    return render(request=request, template_name="webpage/index.html", context=context)