import 'package:flutter/material.dart';
import '../widgets/home/SuspiciousActivityCard.dart';
import '../widgets/home/ProfileGrid.dart';
import '../widgets/home/EditProfiles.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  List<Map<String, List<Map<String, String>>>> profiles = [
    {"Profile1": [{"John Doe": "Friend"}, {"Joh dae": "Family"}]},
    {"Profile2": [{"Jane Doe": "Friend"}, {"Jane dae": "Family"}]},
    {"Profile3": [{"John Smith": "Friend"}, {"John smi": "Family"}]},
    {"Profile4": [{"Jane Smith": "Friend"}, {"Jane smi": "Family"}]},
    {"Profile5": [{"John Doe": "Friend"}, {"John dae": "Family"}]},
  ];

  String? selectedProfile;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            const SuspiciousActivityCard(),
            Expanded(
              child: ProfileGrid(
                profiles: profiles,
                selectedProfile: selectedProfile,
                onProfileSelected: (profileName) {
                  _showConfirmationDialog(context, profileName);
                },
                onEditProfiles: (updatedProfiles) {
                  setState(() {
                    profiles = updatedProfiles;
                  });
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showConfirmationDialog(BuildContext context, String profileName) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Confirmation'),
          content: Text('Are you sure you want to select $profileName?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                setState(() {
                  selectedProfile = profileName;
                });
                Navigator.of(context).pop();
              },
              child: const Text('Confirm'),
            ),
          ],
        );
      },
    );
  }
}
