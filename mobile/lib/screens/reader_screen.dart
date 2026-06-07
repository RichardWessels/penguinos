import 'package:dopios_mobile/api/api_client.dart';
import 'package:dopios_mobile/models/story_translation.dart';
import 'package:flutter/material.dart';

class ReaderScreen extends StatefulWidget {
  const ReaderScreen({
    super.key,
    required this.apiClient,
    required this.translatedStoryPublicId,
  });

  final ApiClient apiClient;
  final String translatedStoryPublicId;

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  ParallelStory? _story;
  String? _error;
  bool _isLoading = true;
  int? _selectedSentenceIndex;
  double _fontSize = 18;
  double _lineHeight = 1.55;
  ReaderTone _tone = ReaderTone.light;

  @override
  void initState() {
    super.initState();
    _loadStory();
  }

  Future<void> _loadStory() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final story = await widget.apiClient.fetchParallelStory(
        widget.translatedStoryPublicId,
      );
      setState(() {
        _story = story;
        _isLoading = false;
      });
    } catch (error) {
      setState(() {
        _error = error.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final tone = _tone.colors;

    return Scaffold(
      backgroundColor: tone.background,
      appBar: AppBar(
        backgroundColor: tone.background,
        foregroundColor: tone.foreground,
        title: Text(_story?.story.title ?? 'Reader'),
        actions: [
          IconButton(
            tooltip: 'Reader settings',
            icon: const Icon(Icons.tune_outlined),
            onPressed: _story == null ? null : _openReaderSettings,
          ),
        ],
      ),
      body: _buildBody(tone),
    );
  }

  Widget _buildBody(_ReaderToneColors tone) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null || _story == null) {
      return ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const SizedBox(height: 80),
          Icon(Icons.error_outline, size: 48, color: tone.accent),
          const SizedBox(height: 16),
          Text(
            'Could not open story',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: tone.foreground,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            _error ?? 'The story could not be loaded.',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: tone.muted,
                ),
          ),
          const SizedBox(height: 20),
          Center(
            child: FilledButton.icon(
              onPressed: _loadStory,
              icon: const Icon(Icons.refresh),
              label: const Text('Try again'),
            ),
          ),
        ],
      );
    }

    final story = _story!;
    final translatedSentences =
        _splitIntoSentences(story.translatedStory.content);
    final originalSentences = _splitIntoSentences(story.originalStory.content);

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
      children: [
        Text(
          story.translatedStory.title,
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                color: tone.foreground,
                fontWeight: FontWeight.w700,
              ),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            _ReaderPill(
              icon: Icons.translate_outlined,
              label: story.translatedStory.language.name,
              tone: tone,
            ),
            _ReaderPill(
              icon: Icons.speed_outlined,
              label: story.translatedStory.difficulty.name,
              tone: tone,
            ),
          ],
        ),
        const SizedBox(height: 24),
        for (int i = 0; i < translatedSentences.length; i++)
          _SentenceBlock(
            translated: translatedSentences[i],
            original:
                i < originalSentences.length ? originalSentences[i] : null,
            isSelected: _selectedSentenceIndex == i,
            fontSize: _fontSize,
            lineHeight: _lineHeight,
            tone: tone,
            onTap: () {
              setState(() {
                _selectedSentenceIndex = _selectedSentenceIndex == i ? null : i;
              });
            },
          ),
      ],
    );
  }

  void _openReaderSettings() {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setSheetState) {
            return Padding(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Reader',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 18),
                  _SettingsSlider(
                    icon: Icons.format_size,
                    label: 'Text size',
                    value: _fontSize,
                    min: 15,
                    max: 24,
                    divisions: 9,
                    onChanged: (value) {
                      setState(() => _fontSize = value);
                      setSheetState(() {});
                    },
                  ),
                  _SettingsSlider(
                    icon: Icons.format_line_spacing,
                    label: 'Line height',
                    value: _lineHeight,
                    min: 1.25,
                    max: 1.9,
                    divisions: 13,
                    onChanged: (value) {
                      setState(() => _lineHeight = value);
                      setSheetState(() {});
                    },
                  ),
                  const SizedBox(height: 8),
                  SegmentedButton<ReaderTone>(
                    segments: const [
                      ButtonSegment(
                        value: ReaderTone.light,
                        icon: Icon(Icons.wb_sunny_outlined),
                      ),
                      ButtonSegment(
                        value: ReaderTone.sepia,
                        icon: Icon(Icons.local_cafe_outlined),
                      ),
                      ButtonSegment(
                        value: ReaderTone.dark,
                        icon: Icon(Icons.dark_mode_outlined),
                      ),
                    ],
                    selected: {_tone},
                    onSelectionChanged: (selection) {
                      setState(() => _tone = selection.first);
                      setSheetState(() {});
                    },
                  ),
                  const SizedBox(height: 16),
                  OutlinedButton.icon(
                    onPressed: () {
                      setState(() => _selectedSentenceIndex = null);
                      Navigator.pop(context);
                    },
                    icon: const Icon(Icons.visibility_off_outlined),
                    label: const Text('Hide translations'),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}

class _SentenceBlock extends StatelessWidget {
  const _SentenceBlock({
    required this.translated,
    required this.original,
    required this.isSelected,
    required this.fontSize,
    required this.lineHeight,
    required this.tone,
    required this.onTap,
  });

  final String translated;
  final String? original;
  final bool isSelected;
  final double fontSize;
  final double lineHeight;
  final _ReaderToneColors tone;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: isSelected ? tone.highlight : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  translated,
                  style: TextStyle(
                    color: tone.foreground,
                    fontSize: fontSize,
                    height: lineHeight,
                  ),
                ),
                if (isSelected && original != null) ...[
                  const SizedBox(height: 8),
                  Text(
                    original!,
                    style: TextStyle(
                      color: tone.translation,
                      fontSize: fontSize - 1,
                      height: lineHeight,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _ReaderPill extends StatelessWidget {
  const _ReaderPill({
    required this.icon,
    required this.label,
    required this.tone,
  });

  final IconData icon;
  final String label;
  final _ReaderToneColors tone;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: tone.pill,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 15, color: tone.foreground),
            const SizedBox(width: 6),
            Text(label, style: TextStyle(color: tone.foreground)),
          ],
        ),
      ),
    );
  }
}

class _SettingsSlider extends StatelessWidget {
  const _SettingsSlider({
    required this.icon,
    required this.label,
    required this.value,
    required this.min,
    required this.max,
    required this.divisions,
    required this.onChanged,
  });

  final IconData icon;
  final String label;
  final double value;
  final double min;
  final double max;
  final int divisions;
  final ValueChanged<double> onChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon),
        const SizedBox(width: 12),
        SizedBox(width: 82, child: Text(label)),
        Expanded(
          child: Slider(
            value: value,
            min: min,
            max: max,
            divisions: divisions,
            onChanged: onChanged,
          ),
        ),
      ],
    );
  }
}

enum ReaderTone { light, sepia, dark }

extension _ReaderTonePalette on ReaderTone {
  _ReaderToneColors get colors {
    switch (this) {
      case ReaderTone.light:
        return const _ReaderToneColors(
          background: Color(0xFFFAFBF8),
          foreground: Color(0xFF17211D),
          muted: Color(0xFF66736C),
          accent: Color(0xFF006D5B),
          highlight: Color(0xFFE5F2ED),
          translation: Color(0xFF006D5B),
          pill: Color(0xFFE7ECE8),
        );
      case ReaderTone.sepia:
        return const _ReaderToneColors(
          background: Color(0xFFF7F0E3),
          foreground: Color(0xFF251D16),
          muted: Color(0xFF746858),
          accent: Color(0xFF6F5D2A),
          highlight: Color(0xFFEDE1C6),
          translation: Color(0xFF6F5D2A),
          pill: Color(0xFFECE0CC),
        );
      case ReaderTone.dark:
        return const _ReaderToneColors(
          background: Color(0xFF111816),
          foreground: Color(0xFFE9F0EC),
          muted: Color(0xFFA7B2AD),
          accent: Color(0xFF8FDAC4),
          highlight: Color(0xFF1E332E),
          translation: Color(0xFF8FDAC4),
          pill: Color(0xFF22312D),
        );
    }
  }
}

class _ReaderToneColors {
  const _ReaderToneColors({
    required this.background,
    required this.foreground,
    required this.muted,
    required this.accent,
    required this.highlight,
    required this.translation,
    required this.pill,
  });

  final Color background;
  final Color foreground;
  final Color muted;
  final Color accent;
  final Color highlight;
  final Color translation;
  final Color pill;
}

List<String> _splitIntoSentences(String text) {
  final matches =
      RegExp(r'[^.!?]+(?:[.!?]+|$)', multiLine: true).allMatches(text);
  final sentences = matches
      .map((match) => match.group(0)?.trim())
      .whereType<String>()
      .where((sentence) => sentence.isNotEmpty)
      .toList();

  return sentences.isEmpty ? [text.trim()] : sentences;
}
