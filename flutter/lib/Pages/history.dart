import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class History extends StatefulWidget {
  const History({super.key});

  @override
  State<History> createState() => _HistoryState();
}

class _HistoryState extends State<History> {
  @override
  Widget build(BuildContext context) {
    Map<String, List<Map<String, String>>> data = {
      "22-07-2024": [
        {"time": "14:00", "name": "John Smith"},
        {"time": "15:00", "name": "Jane Doe"},
      ],
      "23-07-2024": [
        {"time": "12:00", "name": "John"},
        {"time": "13:00", "name": "Jane Smith"},
      ],
      "24-07-2024": [
        {"time": "10:00", "name": "John Doe"},
        {"time": "11:00", "name": "Jane"},
      ],
    };

    List<String> dates = data.keys.toList();
    dates.sort((a, b) => b.compareTo(a));
    DateTime today = DateTime.now();
    DateTime yesterday = today.subtract(const Duration(days: 1));
    DateFormat dateFormat = DateFormat('dd-MMM-yyyy');  // Change format to use abbreviated month

    return Scaffold(
      body: ListView.builder(
        itemCount: dates.length,
        itemBuilder: (context, index) {
          String date = dates[index];
          List<Map<String, String>> details = data[date]!;
          DateTime parsedDate = DateFormat('dd-MM-yyyy').parse(date);

          String displayDate;
          if (parsedDate.isAtSameMomentAs(DateTime(today.year, today.month, today.day))) {
            displayDate = "Today";
          } else if (parsedDate.isAtSameMomentAs(DateTime(yesterday.year, yesterday.month, yesterday.day))) {
            displayDate = "Yesterday";
          } else {
            displayDate = dateFormat.format(parsedDate);  // Format the date with abbreviated month
          }

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Text(
                  displayDate,
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
