from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend


from mainApp.models import Language, Difficulty, StoryTranslation
from mainApp.serializers import (
    LanguageSerializer,
    DifficultySerializer,
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
