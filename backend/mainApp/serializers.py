from mainApp.models import Language, Difficulty, Story, StoryTranslation
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["public_id", "language_name", "language_code"]


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = ["public_id", "difficulty"]


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["public_id", "title"]


class StoryTranslationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryTranslation
        fields = ["public_id", "title", "story", "language", "difficulty"]


class StoryTranslationDetailSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    difficulty = DifficultySerializer(read_only=True)

    class Meta:
        model = StoryTranslation
        fields = ["public_id", "title", "content", "story", "language", "difficulty"]


class ParallelStorySerializer(serializers.Serializer):
    story = StorySerializer()
    original_story = StoryTranslationDetailSerializer()
    translated_story = StoryTranslationDetailSerializer()
