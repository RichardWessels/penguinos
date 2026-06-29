import 'package:dopios_mobile/models/difficulty.dart';
import 'package:dopios_mobile/models/language.dart';
import 'package:dopios_mobile/models/story_translation.dart';
import 'package:flutter/material.dart';

class StoryListItem extends StatelessWidget {
  const StoryListItem({
    super.key,
    required this.story,
    required this.languagesById,
    required this.difficultiesById,
    required this.onTap,
  });

  final StoryTranslationListItem story;
  final Map<String, Language> languagesById;
  final Map<String, Difficulty> difficultiesById;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final language = languagesById[story.languageId];
    final difficulty = difficultiesById[story.difficultyId];

    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      title: Text(
        story.title,
        maxLines: 2,
        overflow: TextOverflow.ellipsis,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.w600,
            ),
      ),
      subtitle: Padding(
        padding: const EdgeInsets.only(top: 6),
        child: Wrap(
          spacing: 8,
          runSpacing: 6,
          children: [
            _MetaPill(
              icon: Icons.translate_outlined,
              label: language?.name ?? 'Language',
            ),
            _MetaPill(
              icon: Icons.speed_outlined,
              label: difficulty?.name ?? 'Level',
            ),
          ],
        ),
      ),
      trailing: const Icon(Icons.chevron_right),
      onTap: onTap,
    );
  }
}

class _MetaPill extends StatelessWidget {
  const _MetaPill({
    required this.icon,
    required this.label,
  });

  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.secondaryContainer.withValues(alpha: 0.55),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 14, color: colorScheme.onSecondaryContainer),
            const SizedBox(width: 5),
            Text(
              label,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: colorScheme.onSecondaryContainer,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
