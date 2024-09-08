import 'package:flutter/material.dart';
import 'Pages/home.dart';
import 'Pages/history.dart';
import 'Pages/people.dart';
//import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // try {
  //   await dotenv.load(fileName: ".env");
  //   print("Loaded .env file");
  // } catch (e) {
  //   print("Error loading .env file: $e");
  // }
  runApp(const SummerProj());
}

class SummerProj extends StatefulWidget {
  const SummerProj({super.key});

  @override
  State<SummerProj> createState() => _SummerProjState();
}

class _SummerProjState extends State<SummerProj> {
  int selectedIndex = 0;
  late PageController _pageController;  // Declare PageController as late

  static const List<Widget> widgetOptions = <Widget>[
    Home(),
    History(),
    People(),
  ];

  @override
  void initState() {
    super.initState();
    // Initialize the PageController
    _pageController = PageController(initialPage: selectedIndex);
  }

  void _onItemTapped(int index) {
    setState(() {
      selectedIndex = index;
    });
    _pageController.animateToPage(
      index,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  void _onPageChanged(int index) {
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
        body: PageView(
          controller: _pageController,
          onPageChanged: _onPageChanged,
          children: widgetOptions,
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

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }
}
