from django.urls import path, include

from rest_framework import routers

from mainApp import views

router = routers.DefaultRouter()
router.register("stories", views.StoryTranslationViewSet, basename="stories")

urlpatterns = [
    path("health", views.health_check, name="health"),
    path("", include(router.urls)),
    path("languages/", views.LanguageListView.as_view()),
    path("difficulties/", views.DifficultyListView.as_view()),
]
