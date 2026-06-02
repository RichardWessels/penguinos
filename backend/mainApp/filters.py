import django_filters
from mainApp.models import StoryTranslation


class StoryTranslationFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(
        field_name="language__language_code", lookup_expr="exact"
    )
    difficulty = django_filters.CharFilter(
        field_name="difficulty__difficulty", lookup_expr="exact"
    )

    class Meta:
        model = StoryTranslation
        fields = ["language", "difficulty"]
