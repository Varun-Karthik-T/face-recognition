import 'package:flutter/material.dart';
import '../utils/register_face.dart';

class People extends StatefulWidget {
  const People({super.key});

  @override
  PeopleState createState() => PeopleState();
}

class PeopleState extends State<People> {
  List<Map<String, String>> peopleList = [
    {"id": "123", "name": "John Doe", "relationship": "Friend"},
    {"id": "124", "name": "Varun", "relationship": "Family"},
    {"id": "125", "name": "Salai", "relationship": "Family"},
    {"id": "126", "name": "Ezhil", "relationship": "Family"},
    {"id": "127", "name": "John Doe", "relationship": "Friend"},
    {"id": "128", "name": "Jane Doe", "relationship": "Family"},
    {"id": "129", "name": "John Smith", "relationship": "Friend"},
    {"id": "130", "name": "Jane Smith", "relationship": "Family"},
    {"id": "131", "name": "John Doe", "relationship": "Friend"},
    {"id": "132", "name": "Jane Doe", "relationship": "Family"},
    {"id": "133", "name": "John Smith", "relationship": "Friend"},
    {"id": "134", "name": "Jane Smith", "relationship": "Family"},
    {"id": "135", "name": "John Doe", "relationship": "Friend"},
    {"id": "136", "name": "Jane Doe", "relationship": "Family"},
    {"id": "137", "name": "John Smith", "relationship": "Friend"},
    {"id": "138", "name": "Jane Smith", "relationship": "Family"},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: peopleList.length,
        itemBuilder: (context, index) {
          return Column(
            children: [
              ListTile(
                leading: CircleAvatar(
                  backgroundColor: Colors.blue[200],
                  child:Text('${peopleList[index]["name"]![0]}',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w300,
                    color: Colors.white,
                  ),
                  ),
                ),
                title: Text(
                  peopleList[index]["name"]!,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    fontFamily: 'Roboto',
                  ),
                ),
                subtitle: Text(
                  peopleList[index]["relationship"]!,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w300,
                  ),
                ),
              ),
              const Divider(
                height: 10,
                thickness: 0.5,
                indent: 20,
                endIndent: 20,
                color: Colors.blueGrey,
              ),
            ],
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const Register()),
          );
        },
        child: const Icon(Icons.add),
        backgroundColor: Colors.blue[200],
      ),
    );
  }
}
