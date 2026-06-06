from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound, ValidationError

from django_filters.rest_framework import DjangoFilterBackend


from mainApp.models import Language, Difficulty, StoryTranslation
from mainApp.serializers import (
    LanguageSerializer,
    DifficultySerializer,
    ParallelStorySerializer,
    StoryTranslationListSerializer,
)
from mainApp.filters import StoryTranslationFilter


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class DifficultyListView(ListAPIView):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class StoryTranslationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class StoryTranslationListView(ListAPIView[StoryTranslation]):
    serializer_class = StoryTranslationListSerializer
    pagination_class = StoryTranslationPagination
    queryset = StoryTranslation.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = StoryTranslationFilter


class ParallelStoryView(APIView):
    def get(self, request):
        translated_story_public_id = request.query_params.get(
            "translated-story-public-id"
        )
        if not translated_story_public_id:
            raise ValidationError(
                {"translated-story-public-id": ("This query parameter is required.")}
            )

        translations = StoryTranslation.objects.select_related(
            "story", "language", "difficulty"
        )
        translated_story = translations.filter(
            public_id=translated_story_public_id
        ).first()
        if translated_story is None:
            raise NotFound("Translated story not found.")

        original_story = translations.filter(
            story=translated_story.story,
            difficulty=translated_story.difficulty,
            language__language_code="en",
        ).first()
        if original_story is None:
            raise NotFound("Original English story not found.")

        serializer = ParallelStorySerializer(
            {
                "story": translated_story.story,
                "original_story": original_story,
                "translated_story": translated_story,
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
