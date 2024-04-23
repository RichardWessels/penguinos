import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dopios',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Dopios Home Screen'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String _textVal = "Waiting for the text :|";

  void _getRandomText(String language) async {
    Uri uri = Uri.http("10.0.2.2:8000", "/api/get_random_text/${language}");

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
      // print(_textVal);
    } catch (error) {
      print(error);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
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
              ElevatedButton(
                onPressed: () {
                  _getRandomText("french");
                },
                child: const Text("Request French Text"),
              ),
              ElevatedButton(
                onPressed: () {
                  _getRandomText("german");
                },
                child: const Text("Request German Text"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
