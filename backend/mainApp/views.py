from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers, status
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


@extend_schema(
    summary="Check API health",
    description="Returns a simple status payload when the API is reachable.",
    tags=["System"],
    responses={
        200: inline_serializer(
            name="HealthCheckResponse",
            fields={"status": serializers.CharField(help_text='Always returns "ok".')},
        )
    },
)
@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="List supported languages",
        description="Returns the languages that can be used when filtering or displaying stories.",
        tags=["Reference data"],
        responses=LanguageSerializer(many=True),
    )
)
class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List story difficulties",
        description="Returns the available difficulty levels for stories.",
        tags=["Reference data"],
        responses=DifficultySerializer(many=True),
    )
)
class DifficultyListView(ListAPIView):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class StoryTranslationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


@extend_schema_view(
    get=extend_schema(
        summary="List story translations",
        description=(
            "Returns paginated story translations. Use the language and difficulty "
            "query parameters to narrow the list for the mobile app."
        ),
        tags=["Stories"],
        parameters=[
            OpenApiParameter(
                name="language",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Language code to filter by, for example `en`, `fr` or `de`.",
            ),
            OpenApiParameter(
                name="difficulty",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Difficulty name to filter by, for example `A2` or `B1`.",
            ),
        ],
        responses=StoryTranslationListSerializer(many=True),
    )
)
class StoryTranslationListView(ListAPIView[StoryTranslation]):
    serializer_class = StoryTranslationListSerializer
    pagination_class = StoryTranslationPagination
    queryset = StoryTranslation.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = StoryTranslationFilter


class ParallelStoryView(APIView):
    @extend_schema(
        summary="Get a translated story with its English original",
        description=(
            "Returns a selected translated story alongside the matching English story "
            "for the same story and difficulty."
        ),
        tags=["Stories"],
        parameters=[
            OpenApiParameter(
                name="translated-story-public-id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Public ID of the translated story to pair with the English original.",
            )
        ],
        responses={
            200: ParallelStorySerializer,
            400: OpenApiResponse(
                description="Missing required `translated-story-public-id` query parameter."
            ),
            404: OpenApiResponse(
                description="Translated story or matching English original was not found."
            ),
        },
        examples=[
            OpenApiExample(
                "Parallel story request",
                value="/api/parallel-story/?translated-story-public-id=7f7bc5e8-9879-40fa-bb6f-8911dc6cde59",
                request_only=True,
            )
        ],
    )
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
