from mainApp.models import LLMTextWithTranslation, Language
from rest_framework import serializers


class LLMTextWithTranslationSerializer(serializers.HyperlinkedModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())

    class Meta:
        model = LLMTextWithTranslation
        fields = ["text", "translation", "language", "original_prompt", "timestamp"]


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ["language_name"]
