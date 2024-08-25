import 'package:flutter/material.dart';

class SuspiciousActivityCard extends StatelessWidget {
  const SuspiciousActivityCard({super.key});

  @override
  Widget build(BuildContext context) {
    return const Card(
      elevation: 4,
      margin: EdgeInsets.only(bottom: 20.0),
      child: Padding(
        padding: EdgeInsets.all(10.0),
        child: Row(
          children: [
            Icon(Icons.warning_amber_rounded, size: 50, color: Colors.red),
            SizedBox(width: 10),
            Text(
              'Suspicious activity found',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.red,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
