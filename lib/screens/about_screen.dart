import 'package:flutter/material.dart';

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("About"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Penguinos", style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),
            Text(
              "Penguinos helps you replace doomscrolling with language learning.\n\n"
              "If you have feedback, please send it to autitiquepenguin@gmail.com :)",
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const Spacer(),
            const Center(
              child: Text("© AutitiquePenguin"),
            ),
          ],
        ),
      ),
    );
  }
}
