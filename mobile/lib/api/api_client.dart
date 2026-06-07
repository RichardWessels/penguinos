import 'dart:convert';

import 'package:dopios_mobile/models/difficulty.dart';
import 'package:dopios_mobile/models/language.dart';
import 'package:dopios_mobile/models/story_translation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

class ApiException implements Exception {
  const ApiException(this.message);

  final String message;

  @override
  String toString() => message;
}

class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Uri _uri(String path, [Map<String, String?> queryParameters = const {}]) {
    final apiUrl = dotenv.env['API_URL']?.replaceAll("'", '').trim();

    if (apiUrl == null || apiUrl.isEmpty) {
      throw const ApiException('API_URL is not configured.');
    }

    final baseUri =
        apiUrl.startsWith('http://') || apiUrl.startsWith('https://')
            ? Uri.parse(apiUrl)
            : Uri(
                scheme: 'http',
                host: apiUrl.split(':').first,
                port: _port(apiUrl));

    final filteredQuery = Map.fromEntries(
      queryParameters.entries.where((entry) {
        final value = entry.value;
        return value != null && value.isNotEmpty;
      }),
    );

    return baseUri.replace(
      path: path,
      queryParameters: filteredQuery.isEmpty ? null : filteredQuery,
    );
  }

  int? _port(String apiUrl) {
    final parts = apiUrl.split(':');
    if (parts.length < 2) {
      return null;
    }
    return int.tryParse(parts.last);
  }

  Future<List<Language>> fetchLanguages() async {
    final json = await _getJson(_uri('/api/languages/'));
    return (json as List<dynamic>)
        .map((item) => Language.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<List<Difficulty>> fetchDifficulties() async {
    final json = await _getJson(_uri('/api/difficulties/'));
    return (json as List<dynamic>)
        .map((item) => Difficulty.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<PaginatedStoryTranslations> fetchStories({
    String? languageCode,
    String? difficultyName,
    int limit = 20,
    int offset = 0,
  }) async {
    final json = await _getJson(
      _uri('/api/stories/', {
        'language': languageCode,
        'difficulty': difficultyName,
        'limit': limit.toString(),
        'offset': offset.toString(),
      }),
    );

    return PaginatedStoryTranslations.fromJson(json as Map<String, dynamic>);
  }

  Future<ParallelStory> fetchParallelStory(
      String translatedStoryPublicId) async {
    final json = await _getJson(
      _uri('/api/parallel-story/', {
        'translated-story-public-id': translatedStoryPublicId,
      }),
    );

    return ParallelStory.fromJson(json as Map<String, dynamic>);
  }

  Future<bool> healthCheck() async {
    final json = await _getJson(_uri('/api/health'));
    return json is Map<String, dynamic> && json['status'] == 'ok';
  }

  Future<dynamic> _getJson(Uri uri) async {
    final response = await _client.get(uri);

    if (response.statusCode >= 400) {
      throw ApiException('Request failed with status ${response.statusCode}.');
    }

    return json.decode(utf8.decode(response.bodyBytes));
  }
}
