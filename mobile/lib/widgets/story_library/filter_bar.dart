import 'package:dopios_mobile/models/difficulty.dart';
import 'package:dopios_mobile/models/language.dart';
import 'package:flutter/material.dart';

class StoryFilterBar extends StatelessWidget {
  const StoryFilterBar({
    super.key,
    required this.languages,
    required this.difficulties,
    required this.selectedLanguage,
    required this.selectedDifficulty,
    required this.onLanguageChanged,
    required this.onDifficultyChanged,
  });

  final List<Language> languages;
  final List<Difficulty> difficulties;
  final Language? selectedLanguage;
  final Difficulty? selectedDifficulty;
  final ValueChanged<Language?> onLanguageChanged;
  final ValueChanged<Difficulty?> onDifficultyChanged;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Theme.of(context).colorScheme.surface,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final languageField = _LanguageField(
            languages: languages,
            selectedLanguage: selectedLanguage,
            onChanged: onLanguageChanged,
          );
          final difficultyField = _DifficultyField(
            difficulties: difficulties,
            selectedDifficulty: selectedDifficulty,
            onChanged: onDifficultyChanged,
          );

          if (constraints.maxWidth < 390) {
            return Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
              child: Column(
                children: [
                  languageField,
                  const SizedBox(height: 10),
                  difficultyField,
                ],
              ),
            );
          }

          return Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
            child: Row(
              children: [
                Expanded(child: languageField),
                const SizedBox(width: 12),
                Expanded(child: difficultyField),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _LanguageField extends StatelessWidget {
  const _LanguageField({
    required this.languages,
    required this.selectedLanguage,
    required this.onChanged,
  });

  final List<Language> languages;
  final Language? selectedLanguage;
  final ValueChanged<Language?> onChanged;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<Language?>(
      initialValue: selectedLanguage,
      isExpanded: true,
      decoration: const InputDecoration(
        labelText: 'Language',
        prefixIcon: Icon(Icons.translate_outlined),
      ),
      items: [
        const DropdownMenuItem<Language?>(
          value: null,
          child: Text('All languages', overflow: TextOverflow.ellipsis),
        ),
        ...languages.map(
          (language) => DropdownMenuItem<Language?>(
            value: language,
            child: Text(language.name, overflow: TextOverflow.ellipsis),
          ),
        ),
      ],
      onChanged: onChanged,
    );
  }
}

class _DifficultyField extends StatelessWidget {
  const _DifficultyField({
    required this.difficulties,
    required this.selectedDifficulty,
    required this.onChanged,
  });

  final List<Difficulty> difficulties;
  final Difficulty? selectedDifficulty;
  final ValueChanged<Difficulty?> onChanged;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<Difficulty?>(
      initialValue: selectedDifficulty,
      isExpanded: true,
      decoration: const InputDecoration(
        labelText: 'Difficulty',
        prefixIcon: Icon(Icons.speed_outlined),
      ),
      items: [
        const DropdownMenuItem<Difficulty?>(
          value: null,
          child: Text('All levels', overflow: TextOverflow.ellipsis),
        ),
        ...difficulties.map(
          (difficulty) => DropdownMenuItem<Difficulty?>(
            value: difficulty,
            child: Text(difficulty.name, overflow: TextOverflow.ellipsis),
          ),
        ),
      ],
      onChanged: onChanged,
    );
  }
}
