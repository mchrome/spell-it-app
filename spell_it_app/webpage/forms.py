from django.forms import ModelForm, Textarea
from tts.models import SentenceCollection
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

class SentenceCollectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = SentenceCollection
        fields = ["name", "sentences"]
        widgets = {
            "sentences": Textarea(attrs={"cols": 80, "rows": 20}),
        }
        labels = {
            "sentences": mark_safe("Type your sentences separated by newline characters here: <br>"),
        }