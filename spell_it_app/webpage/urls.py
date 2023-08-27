from django.urls import path, include

from . import views

app_name = "webpage"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:collection_id>", views.index, name="index_selected_collection"),
    path("result/<int:sentence_id>", views.result, name="result"),
    path("upload_collection", views.upload_collection, name="upload_collection"),
    path("submit_collection", views.submit_collection, name="submit_collection"),
    path("collections", views.collections, name="collections"),
]