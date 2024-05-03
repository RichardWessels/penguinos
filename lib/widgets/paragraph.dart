import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';

class Paragraph extends StatefulWidget {
  const Paragraph({super.key, required this.text, required this.englishText});

  final List<String> text;
  final List<String> englishText;

  @override
  State<Paragraph> createState() => _ParagraphState();
}

class _ParagraphState extends State<Paragraph> {
  int translatedIndex =
      -1; // if a text is clicked and english translation shown, this shows which index to translate

  void _onSentenceTap(int index) {
    print("Clicked on sentence: $index");
    if (translatedIndex == index) {
      setState(() {
        translatedIndex = -1;
      });
    } else {
      setState(() {
        translatedIndex = index;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return RichText(
      text: TextSpan(
        style: DefaultTextStyle.of(context).style,
        children: <TextSpan>[
          for (int i = 0; i < widget.text.length; i++)
            TextSpan(
              text:
                  translatedIndex != i ? widget.text[i] : widget.englishText[i],
              style: translatedIndex != i
                  ? const TextStyle(color: Colors.black)
                  : const TextStyle(color: Colors.red),
              recognizer: TapGestureRecognizer()
                ..onTap = () {
                  _onSentenceTap(i);
                },
            ),
        ],
      ),
    );
  }
}
