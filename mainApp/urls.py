from django.urls import path

from mainApp import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path("get_all_texts", views.get_all_texts, name="get_all_texts"),
    path("get_random_text/<str:language>/<str:difficulty>", views.get_text_of_language, name="get_random_text"),
    path("get_language_list", views.get_language_list, name="get_language_list")
]