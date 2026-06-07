import 'package:dopios_mobile/api/api_client.dart';
import 'package:dopios_mobile/models/difficulty.dart';
import 'package:dopios_mobile/models/language.dart';
import 'package:dopios_mobile/models/story_translation.dart';
import 'package:dopios_mobile/screens/about_screen.dart';
import 'package:dopios_mobile/screens/reader_screen.dart';
import 'package:dopios_mobile/widgets/story_library/filter_bar.dart';
import 'package:dopios_mobile/widgets/story_library/story_list_item.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  static const int _pageSize = 20;

  final ApiClient _apiClient = ApiClient();
  final ScrollController _scrollController = ScrollController();

  List<Language> _languages = [];
  List<Difficulty> _difficulties = [];
  List<StoryTranslationListItem> _stories = [];

  Language? _selectedLanguage;
  Difficulty? _selectedDifficulty;
  bool _isLoadingReferenceData = true;
  bool _isLoadingStories = false;
  bool _hasMoreStories = true;
  int _storyCount = 0;
  String? _error;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_loadMoreNearBottom);
    _loadInitialData();
  }

  @override
  void dispose() {
    _scrollController
      ..removeListener(_loadMoreNearBottom)
      ..dispose();
    super.dispose();
  }

  Future<void> _loadInitialData() async {
    setState(() {
      _isLoadingReferenceData = true;
      _error = null;
    });

    try {
      final languages = await _apiClient.fetchLanguages();
      final difficulties = await _apiClient.fetchDifficulties();

      setState(() {
        _languages = languages;
        _difficulties = difficulties;
        _isLoadingReferenceData = false;
      });

      await _refreshStories();
    } catch (error) {
      setState(() {
        _isLoadingReferenceData = false;
        _error = error.toString();
      });
    }
  }

  Future<void> _refreshStories() async {
    setState(() {
      _stories = [];
      _storyCount = 0;
      _hasMoreStories = true;
      _error = null;
    });

    await _loadStories(reset: true);
  }

  Future<void> _loadStories({bool reset = false}) async {
    if (_isLoadingStories || (!_hasMoreStories && !reset)) {
      return;
    }

    setState(() {
      _isLoadingStories = true;
      _error = null;
    });

    try {
      final page = await _apiClient.fetchStories(
        languageCode: _selectedLanguage?.code,
        difficultyName: _selectedDifficulty?.name,
        limit: _pageSize,
        offset: reset ? 0 : _stories.length,
      );

      setState(() {
        _storyCount = page.count;
        _stories = reset ? page.results : [..._stories, ...page.results];
        _hasMoreStories = page.next != null;
        _isLoadingStories = false;
      });
    } catch (error) {
      setState(() {
        _isLoadingStories = false;
        _error = error.toString();
      });
    }
  }

  void _loadMoreNearBottom() {
    final position = _scrollController.position;
    if (position.extentAfter < 320) {
      _loadStories();
    }
  }

  void _openStory(StoryTranslationListItem story) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ReaderScreen(
          apiClient: _apiClient,
          translatedStoryPublicId: story.publicId,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final languagesById = {
      for (final language in _languages)
        if (language.publicId != null) language.publicId!: language,
    };
    final difficultiesById = {
      for (final difficulty in _difficulties)
        if (difficulty.publicId != null) difficulty.publicId!: difficulty,
    };

    return Scaffold(
      appBar: AppBar(
        title: const Text('Penguinos'),
        actions: [
          IconButton(
            tooltip: 'About',
            icon: const Icon(Icons.info_outline),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const AboutPage()),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          if (!_isLoadingReferenceData)
            StoryFilterBar(
              languages: _languages,
              difficulties: _difficulties,
              selectedLanguage: _selectedLanguage,
              selectedDifficulty: _selectedDifficulty,
              onLanguageChanged: (language) {
                setState(() => _selectedLanguage = language);
                _refreshStories();
              },
              onDifficultyChanged: (difficulty) {
                setState(() => _selectedDifficulty = difficulty);
                _refreshStories();
              },
            ),
          Expanded(
            child: RefreshIndicator(
              onRefresh: _loadInitialData,
              child: _buildBody(languagesById, difficultiesById),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBody(
    Map<String, Language> languagesById,
    Map<String, Difficulty> difficultiesById,
  ) {
    if (_isLoadingReferenceData) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null && _stories.isEmpty) {
      return _StateMessage(
        icon: Icons.cloud_off_outlined,
        title: 'Could not load stories',
        message: _error!,
        actionLabel: 'Try again',
        onAction: _loadInitialData,
      );
    }

    if (_stories.isEmpty && !_isLoadingStories) {
      return _StateMessage(
        icon: Icons.menu_book_outlined,
        title: 'No stories found',
        message: 'Try another language or difficulty.',
        actionLabel: 'Clear filters',
        onAction: () {
          setState(() {
            _selectedLanguage = null;
            _selectedDifficulty = null;
          });
          _refreshStories();
        },
      );
    }

    return ListView.separated(
      controller: _scrollController,
      padding: const EdgeInsets.only(bottom: 20),
      itemCount: _stories.length + 2,
      separatorBuilder: (context, index) => const Divider(height: 1),
      itemBuilder: (context, index) {
        if (index == 0) {
          return Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Text(
              _storyCount == 1 ? '1 story' : '$_storyCount stories',
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
            ),
          );
        }

        final storyIndex = index - 1;
        if (storyIndex >= _stories.length) {
          if (_isLoadingStories) {
            return const Padding(
              padding: EdgeInsets.all(20),
              child: Center(child: CircularProgressIndicator()),
            );
          }

          if (_error != null) {
            return Padding(
              padding: const EdgeInsets.all(16),
              child: OutlinedButton.icon(
                onPressed: _loadStories,
                icon: const Icon(Icons.refresh),
                label: const Text('Load more'),
              ),
            );
          }

          return const SizedBox(height: 16);
        }

        final story = _stories[storyIndex];
        return StoryListItem(
          story: story,
          languagesById: languagesById,
          difficultiesById: difficultiesById,
          onTap: () => _openStory(story),
        );
      },
    );
  }
}

class _StateMessage extends StatelessWidget {
  const _StateMessage({
    required this.icon,
    required this.title,
    required this.message,
    required this.actionLabel,
    required this.onAction,
  });

  final IconData icon;
  final String title;
  final String message;
  final String actionLabel;
  final VoidCallback onAction;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return ListView(
      padding: const EdgeInsets.all(24),
      children: [
        const SizedBox(height: 80),
        Icon(icon, size: 48, color: colorScheme.primary),
        const SizedBox(height: 16),
        Text(
          title,
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 8),
        Text(
          message,
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: colorScheme.onSurfaceVariant,
              ),
        ),
        const SizedBox(height: 20),
        Center(
          child: FilledButton.icon(
            onPressed: onAction,
            icon: const Icon(Icons.refresh),
            label: Text(actionLabel),
          ),
        ),
      ],
    );
  }
}
