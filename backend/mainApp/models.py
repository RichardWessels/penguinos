import uuid

from django.db import models


class LanguageManager(models.Manager):
    """Resolve languages by code during fixture loading."""

    def get_by_natural_key(self, language_code: str) -> "Language":
        return self.get(language_code=language_code)


class DifficultyManager(models.Manager):
    """Resolve difficulties by label during fixture loading."""

    def get_by_natural_key(self, difficulty: str) -> "Difficulty":
        return self.get(difficulty=difficulty)


class PromptManager(models.Manager):
    """Resolve prompts by text during fixture loading."""

    def get_by_natural_key(self, prompt_text: str) -> "Prompt":
        return self.get(prompt_text=prompt_text)


class Language(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    language_name = models.CharField(max_length=32, unique=True)
    language_code = models.CharField(max_length=8, unique=True)

    objects = LanguageManager()

    def __str__(self):
        return str(self.language_name)

    def natural_key(self) -> tuple[str]:
        """Return the language code used for fixture loading."""
        return (self.language_code,)


class Difficulty(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    difficulty = models.CharField(max_length=16, unique=True)

    objects = DifficultyManager()

    def __str__(self):
        return self.difficulty

    def natural_key(self) -> tuple[str]:
        """Return the difficulty label used for fixture loading."""
        return (self.difficulty,)


class Prompt(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    prompt_text = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromptManager()

    def __str__(self):
        return self.prompt_text

    def natural_key(self) -> tuple[str]:
        """Return the prompt text used for fixture loading."""
        return (self.prompt_text,)


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
