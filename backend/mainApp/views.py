from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend


from mainApp.models import Language, Difficulty, StoryTranslation
from mainApp.serializers import LanguageSerializer, DifficultySerializer, StoryTranslationSerializer


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


class StoryTranslationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoryTranslationSerializer
    lookup_field = "public_id"

    queryset: QuerySet[StoryTranslation] = StoryTranslation.objects.select_related(
        "language", "difficulty", "story"
    ).order_by("public_id")  # TODO: order by date added

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "language__language_code": ["exact"],
        "difficulty__difficulty": ["exact"],
    }

    pagination_class = StoryTranslationPagination
