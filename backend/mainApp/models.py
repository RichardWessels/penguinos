from django.db import models


class Language(models.Model):
    language_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.language_name)


class LLMTextWithTranslation(models.Model):
    text = models.TextField()
    translation = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    original_prompt = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LLM Text in {self.language}. Timestamp: {self.timestamp}"
