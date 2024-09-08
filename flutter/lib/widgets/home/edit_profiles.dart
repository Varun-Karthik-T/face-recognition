import 'package:flutter/material.dart';

class EditProfiles extends StatefulWidget {
  final List<Map<String, List<Map<String, String>>>> profiles;
  final Function(List<Map<String, List<Map<String, String>>>>) onProfilesUpdated;

  const EditProfiles({super.key, required this.profiles, required this.onProfilesUpdated});

  @override
  State<EditProfiles> createState() => _EditProfilesState();
}

class _EditProfilesState extends State<EditProfiles> {
  late List<Map<String, List<Map<String, String>>>> profiles;

  @override
  void initState() {
    super.initState();
    profiles = widget.profiles;
  }

  void _addPerson(String profileName, String personName, String relationship) {
    setState(() {
      profiles = profiles.map((profile) {
        if (profile.keys.first == profileName) {
          profile[profileName]!.add({personName: relationship});
        }
        return profile;
      }).toList();
    });
    widget.onProfilesUpdated(profiles);
  }

  void _removePerson(String profileName, String personName) {
    setState(() {
      profiles = profiles.map((profile) {
        if (profile.keys.first == profileName) {
          profile[profileName]!.removeWhere((person) => person.keys.first == personName);
        }
        return profile;
      }).toList();
    });
    widget.onProfilesUpdated(profiles);
  }

  void _renameProfile(String oldName) {
    showDialog(
      context: context,
      builder: (context) {
        final TextEditingController controller = TextEditingController(text: oldName);

        return AlertDialog(
          title: const Text('Rename Profile'),
          content: TextField(
            controller: controller,
            decoration: const InputDecoration(
              hintText: 'Enter new profile name',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                final String newName = controller.text.trim();
                if (newName.isNotEmpty && newName != oldName) {
                  setState(() {
                    profiles = profiles.map((profile) {
                      if (profile.keys.first == oldName) {
                        profile[newName] = profile.remove(oldName)!;
                      }
                      return profile;
                    }).toList();
                  });
                  widget.onProfilesUpdated(profiles);
                }
                Navigator.of(context).pop();
              },
              child: const Text('Rename'),
            ),
          ],
        );
      },
    );
  }

  void _deleteProfile(String profileName) {
    setState(() {
      profiles.removeWhere((profile) => profile.keys.first == profileName);
    });
    widget.onProfilesUpdated(profiles);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Profiles'),
      ),
      body: ListView.builder(
        itemCount: profiles.length,
        itemBuilder: (context, index) {
          String profileName = profiles[index].keys.first;
          List<Map<String, String>> people = profiles[index][profileName]!;

          return Card(
            elevation: 4,
            margin: const EdgeInsets.all(10.0),
            child: ExpansionTile(
              title: Text(profileName),
              trailing: IconButton(
                icon: const Icon(Icons.edit),
                onPressed: () {
                  _renameProfile(profileName);
                },
              ),
              children: [
                ListView.builder(
                  shrinkWrap: true,
                  itemCount: people.length,
                  itemBuilder: (context, personIndex) {
                    String personName = people[personIndex].keys.first;
                    String relationship = people[personIndex][personName]!;

                    return ListTile(
                      title: Text('$personName ($relationship)'),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete, color: Colors.red),
                        onPressed: () {
                          _removePerson(profileName, personName);
                        },
                      ),
                    );
                  },
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: Row(
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          _addPerson(profileName, "New Person", "Friend");
                        },
                        child: const Text('Add Person'),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: () {
                          _deleteProfile(profileName);
                        },
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                        child: const Text('Delete Profile'),

                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
              ],
            ),
          );
        },
      ),
    );
  }
}
