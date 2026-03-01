from rest_framework.response import Response
from rest_framework.decorators import api_view

from mainApp.models import LLMTextWithTranslation, Language
from mainApp.serializers import LLMTextWithTranslationSerializer, LanguageSerializer

import random


def confirm_difficulty(difficulty: str, text: LLMTextWithTranslation):
    '''
    Checks difficulty by looking at prompt text. Used with `filter` to allow only texts of desired difficulty.
    '''
    text_difficulty = "Normal"
    text_prompt: str = text.original_prompt.lower()

    if "a2" in text_prompt:
        text_difficulty = "Easy"

    if "b1" in text_prompt:
        text_difficulty = "Normal"

    if "c1" in text_prompt:
        text_difficulty = "Difficult"
    
    return difficulty == text_difficulty

@api_view(['GET'])
def hello_world(request):
    return Response("Hello world")

@api_view(['GET'])
def get_all_texts(request):
    all_texts = LLMTextWithTranslation.objects.all()
    serializer = LLMTextWithTranslationSerializer(all_texts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_text_of_language(request, language, difficulty):
    language_fk = Language.objects.get(language_name=language)
    language_texts = list(LLMTextWithTranslation.objects.filter(language=language_fk))
    # filter to only allow texts of specified difficulty
    language_texts = list(filter(lambda text: confirm_difficulty(difficulty, text), language_texts))
    item = random.choice(language_texts)
    serializer = LLMTextWithTranslationSerializer(item, many=False, context={'request': request})
    return Response(serializer.data)

# @api_view(['GET'])
# def get_text_of_language(request, language, difficulty):

#     foreign_text = '''Ceci est un exemple de nouvelle utilisée à des fins d’illustration. Pour voir la traduction anglaise, cliquez simplement sur la phrase. Une fois cela fait, la phrase sera écrite en rouge.'''
#     english_text = '''This is an example short story used for illustration. To view the English translation, simply click the sentence. Once this is done, the sentence will be written in red font.'''

#     # foreign_text = '''Um eine Geschichte zum Lesen auszuwählen, wählen Sie aus den unten stehenden Optionen die Sprache und den Schwierigkeitsgrad aus. Wenn Sie beispielsweise „Schwierig“ und „Deutsch“ auswählen, wird eine knifflige deutsche Kurzgeschichte angezeigt. Dies entspricht ungefähr einem Text auf C1-Niveau, der Schwierigkeitsgrad kann jedoch variieren. Sobald die Optionen ausgewählt sind, drücken Sie einfach auf „Anfordern“ und eine Kurzgeschichte wird abgerufen.'''
#     # english_text = '''To select a story to read, choose the language and difficulty from the options below. For example, selecting "Difficult" and "German" will show a tricky German short story. This roughly corresponds to a C1 level text, however, the difficulty may vary. Once the options are selected, simply press "Request" and a short story will be fetched.'''

#     test_entry = LLMTextWithTranslation(text=foreign_text, translation=english_text, 
#                                                     language=None, 
#                                                     original_prompt="")

#     serializer = LLMTextWithTranslationSerializer(test_entry, many=False, context={'request': request})
#     return Response(serializer.data)

@api_view(['GET'])
def get_language_list(request):
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True, context={'request': request})
    return Response(serializer.data)

# @api_view(['GET'])
# def add_random_data(request):
#     new_entry = LLMTextWithTranslation(text=f"Random text: {random.randint(0,100)}", translation=f"Random translation: {random.randint(0,100)}", 
#                                                     language=None, 
#                                                     original_prompt="Some language prompt")
#     new_entry.save()
#     return Response("Data added")