from rest_framework.response import Response
from rest_framework.decorators import api_view

from mainApp.models import LLMTextWithTranslation, Language
from mainApp.serializers import LLMTextWithTranslationSerializer, LanguageSerializer

import random

@api_view(['GET'])
def get_all_texts(request):
    all_texts = LLMTextWithTranslation.objects.all()
    serializer = LLMTextWithTranslationSerializer(all_texts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_text_of_language(request, language):
    language_fk = Language.objects.get(language_name=language)
    language_texts = list(LLMTextWithTranslation.objects.filter(language=language_fk))
    item = random.choice(language_texts)
    serializer = LLMTextWithTranslationSerializer(item, many=False, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_language_list(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True, context={'request': request})
    return Response(serializer.data)