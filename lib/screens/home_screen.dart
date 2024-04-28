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
  String _textVal = "";

  void _getRandomText(String language) async {
    print("Fetching text");
    Uri uri = Uri.http("10.0.2.2:8000", "/api/get_random_text/$language");

    try {
      final res = await http.get(uri);

      if (res.statusCode >= 400) {
        print("ERROR");
        return;
      }

      Map<String, dynamic> llmTextItem =
          json.decode(utf8.decode(res.bodyBytes));
      print(llmTextItem["text"]);
      setState(() {
        _textVal = llmTextItem["text"];
      });
      print(_textVal);
    } catch (error) {
      print(error);
    }
  }

  @override
  Widget build(BuildContext context) {
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
              Text(
                _textVal,
              ),
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
