import 'package:flutter/material.dart';
import 'Pages/home.dart';
import 'Pages/history.dart';
import 'Pages/people.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SummerProj());
}

class SummerProj extends StatefulWidget {
  const SummerProj({super.key});

  @override
  State<SummerProj> createState() => _SummerProjState();
}

class _SummerProjState extends State<SummerProj> {

  int selectedIndex = 0;

  static const List<Widget> widgetOptions = <Widget>[
    Home(),
    History(),
    People(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Summer Project',
      home: Scaffold(
        appBar: AppBar(
          title: Text(
            selectedIndex == 0 ? 'Summer Project' : selectedIndex == 1 ? 'History' : 'People',
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: Colors.lightBlue[800],
        ),
        body: Center(
          child: widgetOptions.elementAt(selectedIndex),
        ),
        bottomNavigationBar: NavigationBar(
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            NavigationDestination(
              icon: Icon(Icons.history),
              label: 'History',
            ),
            NavigationDestination(
              icon: Icon(Icons.people),
              label: 'People',
            ),
          ],
          backgroundColor: Colors.blue[50],
          selectedIndex: selectedIndex,
          onDestinationSelected: _onItemTapped,
          indicatorColor: Colors.lightBlue[700],
        ),
      ),
    );
  }
}
