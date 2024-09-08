import 'package:flutter/material.dart';

class ProfileCard extends StatelessWidget {
  final String profileName;
  final bool isSelected;
  final VoidCallback onTap;

  const ProfileCard({
    super.key,
    required this.profileName,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircleAvatar(
            radius: 30,
            backgroundColor: isSelected ? Colors.green : Colors.blue,
            child: Text(
              profileName[0], // First letter of profile name
              style: const TextStyle(
                fontSize: 24,
                color: Colors.white,
              ),
            ),
          ),
          const SizedBox(height: 8),
          Text(
            profileName,
            style: const TextStyle(fontSize: 16),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
