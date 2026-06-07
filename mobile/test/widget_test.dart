import 'package:dopios_mobile/screens/about_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('About screen renders app identity', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: AboutPage(),
      ),
    );

    expect(find.text('Penguinos'), findsOneWidget);
    expect(find.textContaining('parallel stories'), findsOneWidget);
  });
}
