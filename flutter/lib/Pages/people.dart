import 'package:flutter/material.dart';
import '../widgets/register_face.dart';
import '../api/api.dart';

class People extends StatefulWidget {
  const People({super.key});

  @override
  PeopleState createState() => PeopleState();
}

class PeopleState extends State<People> {
  Future<List<Map<String, dynamic>>> peopleList = Api.getPeople();

  @override
  void initState() {
    super.initState();
    // Ensure the Future is initialized properly
    peopleList = Api.getPeople();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: peopleList,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            print('Error occurred: ${snapshot.error}');
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            print('No data received or list is empty.');
            return const Center(child: Text('No people found.'));
          } else {
            print('Data received: ${snapshot.data}');

            if (snapshot.data!.isNotEmpty) {
              print('First person\'s name: ${snapshot.data![0]["name"]}');
            }

            return ListView.builder(
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                var person = snapshot.data![index];
                return Column(
                  children: [
                    ListTile(
                      leading: CircleAvatar(
                        backgroundColor: Colors.blue[400],
                        child: Text(
                          person["name"][0],
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w300,
                            color: Colors.white,
                          ),
                        ),
                      ),
                      title: Text(
                        person["name"],
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Roboto',
                        ),
                      ),
                      subtitle: Text(
                        person["relationship"],
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w300,
                        ),
                      ),
                    ),
                    const Divider(
                      height: 0,
                      thickness: 0.5,
                      indent: 20,
                      endIndent: 20,
                      color: Colors.blueGrey,
                    ),
                  ],
                );
              },
            );
          }
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        label: const Text('Register face'),
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const Register()),
          );
        },
        icon: const Icon(Icons.add),
        backgroundColor: Colors.blue[200],
      ),
    );
  }
}