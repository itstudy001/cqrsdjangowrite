from django.urls import path
from .views import helloAPI, bookAPI

urlpatterns = [
    path("hello/", helloAPI),
    path("book/", bookAPI)
]