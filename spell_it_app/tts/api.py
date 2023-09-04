from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SentenceCollection
from .serializers import SentenceCollectionSerializer

@api_view(['GET'])
def getCollection(request):
    sentence_collection = SentenceCollection.objects.all()
    serializer = SentenceCollectionSerializer(sentence_collection, many=True)
    return Response(serializer.data)
