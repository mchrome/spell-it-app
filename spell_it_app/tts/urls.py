from django.urls import path
from . import api

urlpatterns = [
    path('get_collection', api.getCollection),
]
