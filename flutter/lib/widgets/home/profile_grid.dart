import 'package:flutter/material.dart';

class ProfileGrid extends StatefulWidget {
  final List<Map<String, dynamic>> profiles;
  final String? selectedProfile;
  final Function(String) onProfileSelected;
  final Function(List<Map<String, dynamic>>) onEditProfiles;

  const ProfileGrid({
    super.key,
    required this.profiles,
    required this.selectedProfile,
    required this.onProfileSelected,
    required this.onEditProfiles,
  });

  @override
  _ProfileGridState createState() => _ProfileGridState();
}

class _ProfileGridState extends State<ProfileGrid> {
  List<Map<String, dynamic>> profilesToEdit = [];

  @override
  void initState() {
    super.initState();
    profilesToEdit = List.from(widget.profiles);
  }

  void _saveEditedProfiles() {
    widget.onEditProfiles(profilesToEdit);
    Navigator.pop(context); // Close the editing dialog
  }

  @override
  Widget build(BuildContext context) {
    return Card(
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
                itemCount: widget.profiles.length + 1, // Add 1 for the pencil icon
                itemBuilder: (context, index) {
                  if (index < widget.profiles.length) {
                    // Fetch profile name from the list
                    String profileName = widget.profiles[index]['name'];
                    return ProfileCard(
                      profileName: profileName,
                      isSelected: widget.selectedProfile == profileName,
                      onTap: () => widget.onProfileSelected(profileName),
                    );
                  } else {
                    // Pencil icon card for editing profiles
                    return GestureDetector(
                      onTap: () {
                        _showEditProfilesDialog(context);
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

  void _showEditProfilesDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Edit Profiles'),
          content: SizedBox(
            width: double.maxFinite,
            child: ListView.builder(
              shrinkWrap: true,
              itemCount: profilesToEdit.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: TextField(
                    controller: TextEditingController(text: profilesToEdit[index]['name']),
                    onChanged: (value) {
                      setState(() {
                        profilesToEdit[index]['name'] = value;
                      });
                    },
                    decoration: InputDecoration(
                      labelText: 'Profile Name ${index + 1}',
                    ),
                  ),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete),
                    onPressed: () {
                      setState(() {
                        profilesToEdit.removeAt(index);
                      });
                    },
                  ),
                );
              },
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context); // Cancel edit
              },
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                _saveEditedProfiles(); // Save profiles and close dialog
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }
}

// ProfileCard Widget
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
      child: Card(
        elevation: isSelected ? 10 : 4,
        child: Center(
          child: Text(
            profileName,
            style: TextStyle(
              fontSize: 16,
              color: isSelected ? Colors.blue : Colors.black,
            ),
          ),
        ),
      ),
    );
  }
}
