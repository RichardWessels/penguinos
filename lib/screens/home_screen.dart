import 'package:dopios_mobile/widgets/paragraph.dart';
import 'package:dopios_mobile/widgets/request_text_buttons.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _originalText = "";
  String _englishText = "";

  void _getRandomText(String language, String difficulty) async {
    Uri uri =
        Uri.http("10.0.2.2:8000", "/api/get_random_text/$language/$difficulty");

    try {
      final res = await http.get(uri);

      if (res.statusCode >= 400) {
        throw "Error fetching text.";
      }

      Map<String, dynamic> llmTextItem =
          json.decode(utf8.decode(res.bodyBytes));
      print(llmTextItem["translation"]);
      setState(() {
        _originalText = llmTextItem["text"];
        _englishText = llmTextItem["translation"];
      });
    } catch (error) {
      setState(() {
        _originalText = error.toString();
      });
    }
  }

  List<String> _splitOnFullStop(String text) {
    // split text on full stop. Then add full stop to end of each element in list
    // if final entry in list != "", then don't add full stop to last entry.
    var splitText = text.split('.');
    for (int i = 0; i < splitText.length - 1; i++) {
      splitText[i] += '.';
    }
    return splitText;
  }

  @override
  Widget build(BuildContext context) {
    Widget paragraphText = const Text("");

    if (_originalText != "") {
      paragraphText = Paragraph(
          text: _splitOnFullStop(_originalText),
          englishText: _splitOnFullStop(_englishText));
    }

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text("Home Page"),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(
          vertical: 16,
          horizontal: 16,
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              paragraphText,
              RequestTextButtons(
                onRequest: _getRandomText,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
