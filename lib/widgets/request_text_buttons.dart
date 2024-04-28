import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// final List<String> listItems = <String>["one", "french", "three"];

class RequestTextButtons extends StatefulWidget {
  const RequestTextButtons({
    super.key,
    required this.onRequest,
  });

  final void Function(String language) onRequest;

  @override
  State<RequestTextButtons> createState() => _RequestTextButtonsState();
}

class _RequestTextButtonsState extends State<RequestTextButtons> {
  final List<String> listItems = <String>[""];
  String? dropdownValue;
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
      listItems.clear();
      for (final lang in languages) {
        listItems.add(lang["language_name"]);
      }
      setState(() {
        dropdownValue = listItems[0];
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
    dropdownValue = listItems[0];
  }

  void _requestText() {
    if (dropdownValue == "") {
      return;
    }
    widget.onRequest(dropdownValue!);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        DropdownButton(
          value: dropdownValue,
          items: listItems
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
              dropdownValue = value!;
            });
          },
        ),
        ElevatedButton(
          onPressed: _requestText,
          child: const Text("Request"),
        ),
      ],
    );
  }
}
