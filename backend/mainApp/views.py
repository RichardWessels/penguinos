from rest_framework.response import Response
from rest_framework.decorators import api_view

from mainApp.models import LLMTextWithTranslation, Language
from mainApp.serializers import LLMTextWithTranslationSerializer, LanguageSerializer

import random


def confirm_difficulty(difficulty: str, text: LLMTextWithTranslation):
    """
    Checks difficulty by looking at prompt text. Used with `filter` to allow only texts of desired difficulty.
    """
    text_difficulty = "Normal"
    text_prompt: str = text.original_prompt.lower()

    if "a2" in text_prompt:
        text_difficulty = "Easy"

    if "b1" in text_prompt:
        text_difficulty = "Normal"

    if "c1" in text_prompt:
        text_difficulty = "Difficult"

    return difficulty == text_difficulty


@api_view(["GET"])
def hello_world(request):
    return Response("Hello world")


@api_view(["GET"])
def get_all_texts(request):
    all_texts = LLMTextWithTranslation.objects.all()
    serializer = LLMTextWithTranslationSerializer(
        all_texts, many=True, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
def get_text_of_language(request, language, difficulty):
    language_fk = Language.objects.get(language_name=language)
    language_texts = list(LLMTextWithTranslation.objects.filter(language=language_fk))
    # filter to only allow texts of specified difficulty
    language_texts = list(
        filter(lambda text: confirm_difficulty(difficulty, text), language_texts)
    )
    item = random.choice(language_texts)
    serializer = LLMTextWithTranslationSerializer(
        item, many=False, context={"request": request}
    )
    return Response(serializer.data)


@api_view(["GET"])
def get_language_list(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True, context={"request": request})
    return Response(serializer.data)
