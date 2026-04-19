from __future__ import annotations

import re
from typing import Any
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator

from mainApp.models import Difficulty, Language


MAX_WORDS_PER_STORY = 300
_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
_TERMINAL_PUNCTUATION = (".", "!", "?")


class StoryLanguageBundle(BaseModel):
    language_code: str = Field(description="ISO-style language code, e.g. en, fr, de")
    title: str = Field(description="Short, engaging title in the target language")
    sentences: list[str] = Field(
        description=(
            "Story as an ordered list of complete sentences. "
            "Do not merge or split sentence meaning compared with the other languages."
        )
    )


class StoryGenerationResponse(BaseModel):
    creative_seed: str = Field(description="A short phrase that inspired the story")
    translations: list[StoryLanguageBundle] = Field(
        description="Translations for each requested language, including English."
    )


@dataclass(frozen=True)
class ValidatedStoryBundle:
    sentence_count: int
    by_language: dict[str, StoryLanguageBundle]


class StoryValidationError(ValueError):
    """Raised when generated stories fail alignment or shape checks."""


def normalize_language_code(code: str) -> str:
    """Normalize a language code for consistent internal comparisons.

    Args:
        code: Raw language code from input.

    Returns:
        The trimmed, lowercase language code.
    """
    return code.strip().lower()


class StoryGenerationOptions(BaseModel):
    stories_per_difficulty: int = Field(gt=0)
    difficulties: list[str]
    languages: list[str]
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_retries: int = Field(gt=0)
    dry_run: bool = False

    @field_validator("difficulties")
    @classmethod
    def _validate_difficulties(cls, value: list[str]) -> list[str]:
        """Normalize and validate requested difficulty labels.

        Args:
            value: Raw difficulty labels supplied by the caller.

        Returns:
            Uppercased, deduplicated difficulty labels preserving order.

        Raises:
            ValueError: If no usable difficulty labels are provided.
        """
        normalized = [item.strip().upper() for item in value if item.strip()]
        if not normalized:
            raise ValueError("At least one difficulty is required")
        # Preserve order and remove duplicates.
        return list(dict.fromkeys(normalized))

    @field_validator("languages")
    @classmethod
    def _validate_languages(cls, value: list[str]) -> list[str]:
        """Normalize and validate requested language codes.

        Args:
            value: Raw language code values supplied by the caller.

        Returns:
            Deduplicated language codes preserving order, always including ``en``.

        Raises:
            ValueError: If no usable language codes are provided.
        """
        normalized = [normalize_language_code(item) for item in value if item.strip()]
        if not normalized:
            raise ValueError("At least one language is required")
        deduplicated = list(dict.fromkeys(normalized))
        if "en" not in deduplicated:
            deduplicated.insert(0, "en")
        return deduplicated

    @field_validator("model")
    @classmethod
    def _validate_model(cls, value: str) -> str:
        """Validate the selected model identifier.

        Args:
            value: Raw model name.

        Returns:
            Trimmed model name.

        Raises:
            ValueError: If the model name is empty after trimming.
        """
        stripped = value.strip()
        if not stripped:
            raise ValueError("Model name cannot be empty")
        return stripped


def build_story_generation_options(
    raw_options: dict[str, Any],
) -> StoryGenerationOptions:
    """Build validated story generation options from command inputs.

    Args:
        raw_options: Raw parsed command options.

    Returns:
        A validated ``StoryGenerationOptions`` instance.
    """
    return StoryGenerationOptions(
        stories_per_difficulty=raw_options["stories_per_difficulty"],
        difficulties=raw_options["difficulties"],
        languages=raw_options["languages"],
        model=raw_options["model"],
        temperature=raw_options["temperature"],
        max_retries=raw_options["max_retries"],
        dry_run=raw_options["dry_run"],
    )


def _split_sentences_from_text(text: str) -> list[str]:
    """Split a story body into sentence candidates.

    Args:
        text: Story text containing sentence-ending punctuation.

    Returns:
        A list of trimmed sentence strings.
    """
    text = text.strip()
    if not text:
        return []
    return [
        part.strip() for part in _SENTENCE_SPLIT_PATTERN.split(text) if part.strip()
    ]


def _word_count(text: str) -> int:
    """Count non-empty whitespace-delimited tokens in text.

    Args:
        text: Input text to count.

    Returns:
        The number of non-empty tokens.
    """
    return len([token for token in text.split() if token.strip()])


def validate_story_bundle(
    response: StoryGenerationResponse,
    expected_language_codes: list[str],
    max_words: int = MAX_WORDS_PER_STORY,
) -> ValidatedStoryBundle:
    """Validate generated multilingual stories for shape and alignment.

    Args:
        response: Structured model output containing translations.
        expected_language_codes: Language codes expected in the response.
        max_words: Exclusive upper bound on words per language story.

    Returns:
        A normalized, validated story bundle indexed by language code.

    Raises:
        StoryValidationError: If language coverage, sentence alignment, punctuation,
            title constraints, or word limits are invalid.
    """
    expected_codes = [normalize_language_code(code) for code in expected_language_codes]
    expected_set = set(expected_codes)

    by_language: dict[str, StoryLanguageBundle] = {}
    for item in response.translations:
        code = normalize_language_code(item.language_code)
        if code in by_language:
            raise StoryValidationError(
                f"Duplicate translation entry for language code: {code}"
            )
        by_language[code] = item

    found_set = set(by_language.keys())
    if found_set != expected_set:
        raise StoryValidationError(
            "Language mismatch. "
            f"Expected={sorted(expected_set)} Found={sorted(found_set)}"
        )

    sentence_count: int | None = None

    for code in expected_codes:
        bundle = by_language[code]

        title = bundle.title.strip()
        if not title:
            raise StoryValidationError(f"Title missing for language: {code}")
        if len(title) > 128:
            raise StoryValidationError(
                f"Title too long for language {code}: {len(title)} chars"
            )

        cleaned_sentences: list[str] = []
        for raw_sentence in bundle.sentences:
            sentence = raw_sentence.strip()
            if not sentence:
                continue
            if not sentence.endswith(_TERMINAL_PUNCTUATION):
                raise StoryValidationError(
                    f"Sentence missing terminal punctuation in language {code}: {sentence!r}"
                )
            cleaned_sentences.append(sentence)

        if not cleaned_sentences:
            raise StoryValidationError(
                f"No valid sentences returned for language: {code}"
            )

        if sentence_count is None:
            sentence_count = len(cleaned_sentences)
        elif len(cleaned_sentences) != sentence_count:
            raise StoryValidationError(
                f"Sentence count mismatch for {code}. "
                f"Expected={sentence_count}, Found={len(cleaned_sentences)}"
            )

        content = " ".join(cleaned_sentences)
        if _word_count(content) >= max_words:
            raise StoryValidationError(
                f"Story too long for {code}. Limit={max_words - 1} words, Found={_word_count(content)}"
            )

        split_back = _split_sentences_from_text(content)
        if len(split_back) != len(cleaned_sentences):
            raise StoryValidationError(
                "Sentence splitting mismatch after reconstruction "
                f"for {code}. Sentences must be clearly separated."
            )

        by_language[code] = StoryLanguageBundle(
            language_code=code,
            title=title,
            sentences=cleaned_sentences,
        )

    if sentence_count is None:
        raise StoryValidationError("No sentences produced in story bundle")

    return ValidatedStoryBundle(sentence_count=sentence_count, by_language=by_language)


def generate_validated_bundle(
    chain: Any,
    *,
    difficulty: str,
    language_codes: list[str],
    seed: str,
    retries: int,
):
    """Generate a story bundle with retry logic and strict validation.

    Args:
        chain: LangChain runnable that returns ``StoryGenerationResponse``.
        difficulty: Requested CEFR difficulty level.
        language_codes: Language codes to include in output.
        seed: Creative seed phrase to guide generation.
        retries: Maximum generation attempts before failing.

    Returns:
        A tuple of ``(raw_response, validated_bundle)``.

    Raises:
        StoryValidationError: If all attempts fail invocation or validation.
    """
    latest_error = None
    for _ in range(retries):
        try:
            data = chain.invoke(
                {
                    "difficulty": difficulty,
                    "language_codes_csv": ", ".join(language_codes),
                    "creative_seed": seed,
                    "max_words": 299,
                }
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            latest_error = exc
            continue
        try:
            validated = validate_story_bundle(
                response=data,
                expected_language_codes=language_codes,
                max_words=300,
            )
            return data, validated
        except StoryValidationError as exc:
            latest_error = exc
    raise StoryValidationError(
        "Model output failed sentence alignment checks after "
        f"{retries} retries: {latest_error}"
    )


def get_or_create_languages(
    codes: list[str], language_name_map: dict[str, str]
) -> dict[str, Language]:
    """Fetch or create Language rows for the provided language codes.

    Args:
        codes: Language codes to resolve.
        language_name_map: Mapping from language code to display name.

    Returns:
        A mapping from language code to ``Language`` model instance.
    """
    language_map: dict[str, Language] = {}
    for code in codes:
        language_obj = Language.objects.filter(language_code=code).first()
        if language_obj is None:
            language_name = language_name_map.get(code, code.upper())
            language_obj = Language.objects.create(
                language_code=code,
                language_name=language_name,
            )
        language_map[code] = language_obj
    return language_map


def get_or_create_difficulties(items: list[str]) -> dict[str, Difficulty]:
    """Fetch or create Difficulty rows for requested levels.

    Args:
        items: Difficulty labels to resolve.

    Returns:
        A mapping from difficulty label to ``Difficulty`` model instance.
    """
    difficulty_map: dict[str, Difficulty] = {}
    for difficulty in items:
        difficulty_obj, _ = Difficulty.objects.get_or_create(difficulty=difficulty)
        difficulty_map[difficulty] = difficulty_obj
    return difficulty_map
