import 'package:flutter/material.dart';
import 'ProfileCard.dart';
import 'EditProfiles.dart';

class ProfileGrid extends StatelessWidget {
  final List<Map<String, List<Map<String, String>>>> profiles;
  final String? selectedProfile;
  final Function(String) onProfileSelected;
  final Function(List<Map<String, List<Map<String, String>>>>) onEditProfiles;

  const ProfileGrid({
    super.key,
    required this.profiles,
    required this.selectedProfile,
    required this.onProfileSelected,
    required this.onEditProfiles,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      height: 300,
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Profiles',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  childAspectRatio: 1,
                ),
                itemCount: profiles.length + 1, // Add 1 for the pencil icon
                itemBuilder: (context, index) {
                  if (index < profiles.length) {
                    // Fetch profile name from the list
                    String profileName = profiles[index].keys.first;
                    return ProfileCard(
                      profileName: profileName,
                      isSelected: selectedProfile == profileName,
                      onTap: () => onProfileSelected(profileName),
                    );
                  } else {
                    // Pencil icon card for editing profiles
                    return GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => EditProfiles(
                              profiles: profiles,
                              onProfilesUpdated: onEditProfiles,
                            ),
                          ),
                        );
                      },
                      child: const Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircleAvatar(
                            radius: 30,
                            backgroundColor: Colors.grey,
                            child: Icon(Icons.edit, color: Colors.white, size: 30),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Edit Profiles',
                            style: TextStyle(fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    );
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
