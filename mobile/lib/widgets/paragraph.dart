import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

class Paragraph extends StatefulWidget {
  const Paragraph({super.key, required this.text, required this.englishText});

  final List<String> text;
  final List<String> englishText;

  @override
  State<Paragraph> createState() => _ParagraphState();
}

class _ParagraphState extends State<Paragraph> {
  int translatedIndex = -1;

  void _onSentenceTap(int index) {
    setState(() {
      translatedIndex = translatedIndex == index ? -1 : index;
    });
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
              style: TextStyle(
                fontSize: 16,
                color: translatedIndex != i ? Colors.black87 : Colors.red,
              ),
              recognizer: TapGestureRecognizer()
                ..onTap = () => _onSentenceTap(i),
            ),
        ],
      ),
    );
  }
}
