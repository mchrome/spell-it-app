from django.urls import path, include

from . import views

app_name = "webpage"
urlpatterns = [
    # ex: /webpage/
    path("", views.index, name="index"),
]