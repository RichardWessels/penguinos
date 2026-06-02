from mainApp.models import Language, Difficulty, StoryTranslation
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["public_id", "language_name", "language_code"]


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = ["public_id", "difficulty"]

class StoryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryTranslation
        fields = ["public_id", "title", "content", "story", "language", "difficulty"]
