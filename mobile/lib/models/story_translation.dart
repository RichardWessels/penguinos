import 'package:dopios_mobile/models/difficulty.dart';
import 'package:dopios_mobile/models/language.dart';

class StoryTranslationListItem {
  const StoryTranslationListItem({
    required this.publicId,
    required this.title,
    required this.storyId,
    required this.languageId,
    required this.difficultyId,
  });

  final String publicId;
  final String title;
  final String storyId;
  final String languageId;
  final String difficultyId;

  factory StoryTranslationListItem.fromJson(Map<String, dynamic> json) {
    return StoryTranslationListItem(
      publicId: json['public_id'] as String,
      title: json['title'] as String,
      storyId: json['story'] as String,
      languageId: json['language'] as String,
      difficultyId: json['difficulty'] as String,
    );
  }
}

class PaginatedStoryTranslations {
  const PaginatedStoryTranslations({
    required this.count,
    required this.next,
    required this.previous,
    required this.results,
  });

  final int count;
  final String? next;
  final String? previous;
  final List<StoryTranslationListItem> results;

  factory PaginatedStoryTranslations.fromJson(Map<String, dynamic> json) {
    return PaginatedStoryTranslations(
      count: json['count'] as int,
      next: json['next'] as String?,
      previous: json['previous'] as String?,
      results: (json['results'] as List<dynamic>)
          .map((item) => StoryTranslationListItem.fromJson(
                item as Map<String, dynamic>,
              ))
          .toList(),
    );
  }
}

class StorySummary {
  const StorySummary({
    this.publicId,
    required this.title,
  });

  final String? publicId;
  final String title;

  factory StorySummary.fromJson(Map<String, dynamic> json) {
    return StorySummary(
      publicId: json['public_id'] as String?,
      title: json['title'] as String,
    );
  }
}

class StoryTranslationDetail {
  const StoryTranslationDetail({
    required this.publicId,
    required this.title,
    required this.content,
    required this.storyId,
    required this.language,
    required this.difficulty,
  });

  final String publicId;
  final String title;
  final String content;
  final String storyId;
  final Language language;
  final Difficulty difficulty;

  factory StoryTranslationDetail.fromJson(Map<String, dynamic> json) {
    return StoryTranslationDetail(
      publicId: json['public_id'] as String,
      title: json['title'] as String,
      content: json['content'] as String,
      storyId: json['story'] as String,
      language: Language.fromJson(json['language'] as Map<String, dynamic>),
      difficulty:
          Difficulty.fromJson(json['difficulty'] as Map<String, dynamic>),
    );
  }
}

class ParallelStory {
  const ParallelStory({
    required this.story,
    required this.originalStory,
    required this.translatedStory,
  });

  final StorySummary story;
  final StoryTranslationDetail originalStory;
  final StoryTranslationDetail translatedStory;

  factory ParallelStory.fromJson(Map<String, dynamic> json) {
    return ParallelStory(
      story: StorySummary.fromJson(json['story'] as Map<String, dynamic>),
      originalStory: StoryTranslationDetail.fromJson(
        json['original_story'] as Map<String, dynamic>,
      ),
      translatedStory: StoryTranslationDetail.fromJson(
        json['translated_story'] as Map<String, dynamic>,
      ),
    );
  }
}
