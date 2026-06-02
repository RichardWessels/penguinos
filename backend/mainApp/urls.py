from django.urls import path

from mainApp import views


urlpatterns = [
    path("health", views.health_check, name="health"),
    path("languages/", views.LanguageListView.as_view()),
    path("difficulties/", views.DifficultyListView.as_view()),
    path("stories/", views.StoryTranslationListView.as_view()),
]
