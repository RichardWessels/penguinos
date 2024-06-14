import os
import sys
import django
import ollama

if __name__ == '__main__':

    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(project_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dopios_backend.settings')
    django.setup()

    from mainApp.models import LLMTextWithTranslation, Language


    NUMBER_STORIES_TO_GENERATE = 2
    LANGUAGES = ["german", "french"]
    DIFFICULTIES = ["A2", "B1", "C1"]

    language_foreign_key_dict = {}
    for language in LANGUAGES:
        try:
            Language.objects.get(language_name=language)
        except:
            new_lang = Language(language_name=language)
            new_lang.save()
        
        language_foreign_key_dict[language] = Language.objects.get(language_name=language)


    # get themes
    themes = []
    # prompt = f'Provide me with {NUMBER_STORIES_TO_GENERATE} very simple story themes. Only output the list without any other text. Format the list of themes by having [START] preceeding each list item. Only provide one sentence for each theme, no further text.'
    prompt = f"Provide me with {NUMBER_STORIES_TO_GENERATE} very simple story themes. Only output the list without any other text. Format the list of themes as follows: [START] item 1 [END], [START] item 2 [END]. Ensure this format is followed. Only provide one sentence for each theme"

    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    generated_themes_string = response['message']['content']

    print("UNCLEANED THEME RESPONSE:")
    print(generated_themes_string)

    generated_themes_cleaned = generated_themes_string.rstrip('\n')
    generated_themes_cleaned = generated_themes_cleaned.split("[START]")[1:]
    generated_themes_cleaned = list(map(lambda e: e.split('[END]')[0], generated_themes_cleaned))

    for i, theme in enumerate(generated_themes_cleaned):
        print(f"{i}: {theme}")
        themes.append(theme)

    # Ensure themes are created right
    if not input("PROCEED? (y/N): ").lower().startswith('y'):
        exit(0)

    for theme in themes:
        for language in LANGUAGES:
            for difficulty in DIFFICULTIES:

                try:

                    language_prompt = f"Write an {difficulty} level text in {language} of around 150 words. Output only the {language} followed by the translation. For both the original and translated story, use the format [START] before the start of the story, and [END] at the end. Write about the following theme: {theme}"

                    response = ollama.chat(model='llama3', messages=[
                    {
                        'role': 'user',
                        'content': language_prompt,
                    },
                    ])
                    generated_language_output = response['message']['content']

                    split_text = generated_language_output.split("[START]")

                    original_extracted = split_text[1].split("[END]")[0].strip()
                    translated_extracted = split_text[2].split("[END]")[0].strip()

                    # Verify data by using length
                    if len(original_extracted) < 80 or len(translated_extracted) < 80:
                        raise Exception("Error with prompt output format")
                    
                    # Ensure same number of sentences. Useful to avoid sentences containing Mr. or Dr. which breaks frontend.
                    if len(original_extracted.split('.')) != len(translated_extracted.split('.')):
                        raise Exception("Error with number of sentences")

                    # print("Original::")
                    # print(original_extracted)

                    # print("TRANSLATED")
                    # print(translated_extracted)

                    new_entry = LLMTextWithTranslation(text=original_extracted, translation=translated_extracted, 
                                                        language=language_foreign_key_dict[language], 
                                                        original_prompt=language_prompt)
                    new_entry.save()
                    
                    print(f"STORY ADDED ({language}, {difficulty})")

                except Exception as e:
                    print("Following error occured:")
                    print(e)