import random
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from mainApp.models import Prompt, Story, StoryTranslation
from mainApp.story_generation import (
    StoryGenerationOptions,
    StoryGenerationResponse,
    StoryValidationError,
    build_story_generation_options,
    generate_validated_bundle,
    get_or_create_difficulties,
    get_or_create_languages
)
from mainApp.prompts.story_generation_prompts import system_prompt, user_prompt

DEFAULT_DIFFICULTIES = ["A1", "A2", "B1", "B2"]
DEFAULT_LANGUAGE_CODES = ["en", "fr", "de"]
DEFAULT_STORIES_PER_DIFFICULTY = 1
DEFAULT_MODEL = "gpt-5-mini"

LANGUAGE_NAME_MAP = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
}

CREATIVE_SEEDS = [
    "a city where all clocks are 7 minutes early",
    "a tiny museum of objects found in library books",
    "a train stop that appears only in rain",
    "a baker who receives anonymous map fragments",
    "a lighthouse keeper who is afraid of the ocean",
    "a school project that accidentally predicts tomorrow",
    "a rooftop garden shared by strangers",
    "a violin case delivered to the wrong apartment",
    "a market where nobody is allowed to bargain",
    "a message hidden in old weather reports",
]

class Command(BaseCommand):
    help = (
        "Generate short, multilingual stories (with aligned sentences) with LangChain and save them as "
        "Story + StoryTranslation objects."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--stories-per-difficulty",
            type=int,
            default=DEFAULT_STORIES_PER_DIFFICULTY,
            help=(
                "How many stories to create for each difficulty "
                f"(default: {DEFAULT_STORIES_PER_DIFFICULTY})."
            ),
        )
        parser.add_argument(
            "--difficulties",
            nargs="+",
            default=DEFAULT_DIFFICULTIES,
            help="Difficulty labels to generate (default: A1 A2 B1 B2).",
        )
        parser.add_argument(
            "--languages",
            nargs="+",
            default=DEFAULT_LANGUAGE_CODES,
            help="Language codes to generate (English is forced for alignment).",
        )
        parser.add_argument(
            "--model",
            default=DEFAULT_MODEL,
            help=f"OpenAI chat model (default: {DEFAULT_MODEL}).",
        )
        parser.add_argument(
            "--temperature",
            type=float,
            default=1.0,
            help="Sampling temperature (default: 1.0).",
        )
        parser.add_argument(
            "--max-retries",
            type=int,
            default=3,
            help="Retries per story generation attempt (default: 3).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Generate and validate, but do not write objects to the database.",
        )

    def handle(self, *args, **options):
        if not os.getenv("OPENAI_API_KEY"):
            raise CommandError("OPENAI_API_KEY is required to run this command")

        try:
            generation_options: StoryGenerationOptions = build_story_generation_options(
                options
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        llm = ChatOpenAI(
            model=generation_options.model,
            temperature=generation_options.temperature,
        )
        generation_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )
        chain = generation_prompt | llm.with_structured_output(StoryGenerationResponse)

        language_map = get_or_create_languages(generation_options.languages, LANGUAGE_NAME_MAP)
        difficulty_map = get_or_create_difficulties(
            generation_options.difficulties
        )

        total_attempts = (
            len(generation_options.difficulties)
            * generation_options.stories_per_difficulty
        )
        completed = 0
        created_story_count = 0
        created_translation_count = 0

        self.stdout.write(
            self.style.NOTICE(
                f"Generating {total_attempts} stories across difficulties={generation_options.difficulties} "
                f"and languages={generation_options.languages}."
            )
        )

        for difficulty in generation_options.difficulties:
            for _ in range(generation_options.stories_per_difficulty):
                completed += 1
                seed = random.choice(CREATIVE_SEEDS)
                self.stdout.write(
                    f"[{completed}/{total_attempts}] Difficulty={difficulty} Seed={seed}"
                )

                try:
                    data, validated = generate_validated_bundle(
                        chain,
                        difficulty=difficulty,
                        language_codes=generation_options.languages,
                        seed=seed,
                        retries=generation_options.max_retries,
                    )
                except StoryValidationError as exc:
                    self.stdout.write(
                        self.style.WARNING(
                            "Skipping story due to repeated validation failure: "
                            f"difficulty={difficulty}, seed={seed}, error={exc}"
                        )
                    )
                    continue

                english_bundle = validated.by_language["en"]
                generated_prompt_text = (
                    f"difficulty={difficulty}; languages={','.join(generation_options.languages)}; "
                    f"seed={data.creative_seed}; sentence_count={validated.sentence_count}; "
                    f"theme={seed}"
                )

                if generation_options.dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            "Dry run: validated story with "
                            f"{validated.sentence_count} aligned sentences."
                        )
                    )
                    continue

                with transaction.atomic():
                    story = Story.objects.create(title=english_bundle.title)
                    prompt = Prompt.objects.create(prompt_text=generated_prompt_text)

                    for code in generation_options.languages:
                        translation_bundle = validated.by_language[code]
                        StoryTranslation.objects.create(
                            story=story,
                            language=language_map[code],
                            difficulty=difficulty_map[difficulty],
                            prompt=prompt,
                            title=translation_bundle.title,
                            content=" ".join(translation_bundle.sentences),
                        )
                        created_translation_count += 1

                    created_story_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Completed generation. "
                f"Stories created={created_story_count}, "
                f"translations created={created_translation_count}."
            )
        )
