import 'package:flutter/material.dart';
import '../widgets/home/suspicious_activity_card.dart';
import '../api/api.dart';
import '../widgets/home/profile_grid.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  List<Map<String, dynamic>> profiles = [];
  String? selectedProfile;

  @override
  void initState() {
    super.initState();
    _fetchProfiles();
  }

  Future<void> _fetchProfiles() async {
    try {
      var data = await Api.fetchProfiles();
      setState(() {
        profiles = List<Map<String, dynamic>>.from(data['profiles']);
      });
    } catch (e) {
      print('Error fetching profiles: $e');
    }
  }

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
