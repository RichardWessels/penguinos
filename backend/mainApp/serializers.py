from mainApp.models import Language, StoryTranslation
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["language_code", "language_name"]


class StoryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryTranslation
        fields = ["title", "content", "story", "language", "difficulty"]
