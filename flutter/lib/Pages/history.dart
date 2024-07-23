import 'package:flutter/material.dart';

class History extends StatefulWidget {
  const History({super.key});

  @override
  State<History> createState() => _HistoryState();
}

class _HistoryState extends State<History> {
  @override
  Widget build(BuildContext context) {
    Map<String, List<Map<String, String>>> data = {
      "23-7-2023": [
        {"time": "14:00", "name": "John Smith"},
        {"time": "15:00", "name": "Jane Doe"},
      ],
      "22-7-2023": [
        {"time": "12:00", "name": "John Doe"},
        {"time": "13:00", "name": "Jane Smith"},
      ],
    };

    List<String> dates = data.keys.toList();

    return Scaffold(
      body: ListView.builder(
        itemCount: dates.length,
        itemBuilder: (context, index) {
          String date = dates[index];
          List<Map<String, String>> details = data[date]!;

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Text(
                  date,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Card(
                color: Colors.blue[50],
                margin: const EdgeInsets.all(10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(5.0),
                      child: Column(
                        children: details.asMap().entries.map((entry) {
                          int detailIndex = entry.key;
                          Map<String, String> detail = entry.value;
                          return Column(
                            children: [
                              ListTile(
                                title: Text(
                                  detail['name']!,
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.w600,
                                    fontFamily: 'Roboto',
                                  ),
                                ),
                                subtitle: Text('Time: ${detail['time']}'),
                              ),
                              if (detailIndex != details.length - 1)
                                const Divider(
                                  height: 3,
                                  thickness: 0.5,
                                  indent: 20,
                                  endIndent: 20,
                                  color: Colors.blueGrey,
                                ),
                            ],
                          );
                        }).toList(),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

