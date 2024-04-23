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


    # languages
    languages = ["german", "french"]

    language_foreign_key_dict = {}
    for language in languages:
        try:
            Language.objects.get(language_name=language)
        except:
            new_lang = Language(language_name=language)
            new_lang.save()
        
        language_foreign_key_dict[language] = Language.objects.get(language_name=language)


    # get themes
    themes = []
    prompt = 'Provide me with 5 very simple story themes. Only output the list without any other text. Format the list of themes by having [START] preceeding each list item. Only provide one sentence for each theme, no further text.'

    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    generated_themes_string = response['message']['content']

    for theme in generated_themes_string.split("[START]")[1:]:
        print(theme.rstrip('\n'))
        themes.append(theme.rstrip('\n'))


    for theme in themes:
        for language in languages:

            try:

                language_prompt = f"Write an A2 level text in {language} of around 150 words. Output only the {language} followed by the translation. For both the original and translated story, use the format [START] before the start of the story, and [END] at the end. Write about the following theme: {theme}"

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
                    raise "Error with prompt output format"

                # print("Original::")
                # print(original_extracted)

                # print("TRANSLATED")
                # print(translated_extracted)

                new_entry = LLMTextWithTranslation(text=original_extracted, translation=translated_extracted, 
                                                    language=language_foreign_key_dict[language], 
                                                    original_prompt=language_prompt)
                new_entry.save()
                
                print("STORY ADDED")

            except Exception as e:
                print("Following error occured:")
                print(e)