from rest_framework import serializers
from .models import SentenceCollection

class SentenceCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentenceCollection
        fields = '__all__'