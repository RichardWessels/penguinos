import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// final List<String> listItems = <String>["one", "french", "three"];

class RequestTextButtons extends StatefulWidget {
  const RequestTextButtons({
    super.key,
    required this.onRequest,
  });

  final void Function(String language, String difficulty) onRequest;

  @override
  State<RequestTextButtons> createState() => _RequestTextButtonsState();
}

class _RequestTextButtonsState extends State<RequestTextButtons> {
  final List<String> _languageDropdownItems = <String>[""];
  final List<String> _difficultyDropdownItems = <String>[
    "Easy",
    "Normal",
    "Difficult"
  ];

  String? _languageDropdownValue;
  String? _difficultyDropdownValue;
  bool isFetched = false;
  String? fetchError;

  void _fetchLanguages() async {
    print("Fetching languages");
    Uri uri = Uri.http("10.0.2.2:8000", "/api/get_language_list");

    try {
      final res = await http.get(uri);

      if (res.statusCode >= 400) {
        throw res.statusCode;
      }

      final List<dynamic> languages = json.decode(res.body);
      _languageDropdownItems.clear();
      for (final lang in languages) {
        _languageDropdownItems.add(lang["language_name"]);
      }
      setState(() {
        _languageDropdownValue = _languageDropdownItems[0];
      });
    } catch (error) {
      print(error);
      setState(() {
        fetchError = error.toString();
      });
    }
  }

  String capitalizeString(String str) {
    if (str.isEmpty) {
      return str;
    }
    return str[0].toUpperCase() + str.substring(1);
  }

  @override
  void initState() {
    super.initState();
    _fetchLanguages();
    _languageDropdownValue = _languageDropdownItems[0];
    _difficultyDropdownValue =
        _difficultyDropdownItems[1]; // set difficulty to normal
  }

  void _requestText() {
    if (_languageDropdownValue == "") {
      return;
    }
    widget.onRequest(_languageDropdownValue!, _difficultyDropdownValue!);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        DropdownButton(
          value: _languageDropdownValue,
          items: _languageDropdownItems
              .map<DropdownMenuItem<String>>(
                (item) => DropdownMenuItem(
                  value: item,
                  child: Text(
                    capitalizeString(item),
                  ),
                ),
              )
              .toList(),
          onChanged: (String? value) {
            setState(() {
              _languageDropdownValue = value!;
            });
          },
        ),
        const SizedBox(
          width: 16,
        ),
        DropdownButton(
          value: _difficultyDropdownValue,
          items: _difficultyDropdownItems
              .map<DropdownMenuItem<String>>(
                (item) => DropdownMenuItem(
                  value: item,
                  child: Text(
                    capitalizeString(item),
                  ),
                ),
              )
              .toList(),
          onChanged: (String? value) {
            setState(() {
              _difficultyDropdownValue = value!;
            });
          },
        ),
        const SizedBox(
          width: 16,
        ),
        ElevatedButton(
          onPressed: _requestText,
          child: const Text("Request"),
        ),
      ],
    );
  }
}
