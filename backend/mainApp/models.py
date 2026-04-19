import uuid

from django.db import models


class Language(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    language_name = models.CharField(max_length=32, unique=True)
    language_code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return str(self.language_name)


class Difficulty(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    difficulty = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.difficulty


class Prompt(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt_text


class Story(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class StoryTranslation(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["story", "language", "difficulty"],
                name="unique_story_language_difficulty",
            )
        ]
