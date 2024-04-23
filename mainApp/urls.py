from django.urls import path

from mainApp import views

urlpatterns = [
    path("get_all_texts", views.get_all_texts, name="get_all_texts"),
    path("get_random_text/<str:language>/", views.get_text_of_language, name="get_random_text")
]