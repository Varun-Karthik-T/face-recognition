import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import '../api/api.dart';

class History extends StatefulWidget {
  const History({super.key});

  @override
  State<History> createState() => _HistoryState();
}

class _HistoryState extends State<History> {
  late Future<Map<String, List<Map<String, String>>>> futureData;

  @override
  void initState() {
    super.initState();
    futureData = fetchHistoryData();
  }


  Future<Map<String, List<Map<String, String>>>> fetchHistoryData() async {
    try {
      // Fetching the raw response from the API
      final response = await Api.fetchHistory();

      // Check if the response was successful
      if (response.statusCode == 200) {
        // Parse the response body as JSON
        dynamic data = jsonDecode(response.body);

        // Reformatting data to the required format
        Map<String, List<Map<String, String>>> historyData = {};

        for (var item in data) {
          String date = DateFormat('EEE, dd MMM yyyy HH:mm:ss')
              .parse(item['date'])
              .toString()
              .split(' ')[0];  // Extract the date in the format yyyy-MM-dd

          List<Map<String, String>> details = (item['entries'] as List).map((entry) {
            return {
              "name": entry['name'].toString(),
              "time": DateFormat('HH:mm').format(
                  DateFormat('EEE, dd MMM yyyy HH:mm:ss')
                      .parse(entry['timestamp'].toString())
              ),
            };
          }).toList();

          historyData[date] = details;
        }
        return historyData;
      } else {
        throw Exception('Failed to load history data');
      }
    } catch (error) {
      throw Exception('Unable to fetch history');
    }
  }



  @override
  Widget build(BuildContext context) {
    DateTime today = DateTime.now();
    DateTime yesterday = today.subtract(const Duration(days: 1));
    DateFormat dateFormat = DateFormat('dd-MMM-yyyy');

    return Scaffold(
      body: FutureBuilder<Map<String, List<Map<String, String>>>>(
        future: futureData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator()); // Loading state
          } else if (snapshot.hasError) {
            return const Center(child: Text('Unable to fetch history')); // Error state
          } else if (snapshot.hasData) {
            Map<String, List<Map<String, String>>> data = snapshot.data!;
            List<String> dates = data.keys.toList();
            dates.sort((a, b) => b.compareTo(a)); // Sort dates in descending order

            return ListView.builder(
              itemCount: dates.length,
              itemBuilder: (context, index) {
                String date = dates[index];
                List<Map<String, String>> details = data[date]!;
                DateTime parsedDate = DateTime.parse(date); // Use DateTime.parse as the format is yyyy-MM-dd

                String displayDate;
                if (parsedDate.isAtSameMomentAs(DateTime(today.year, today.month, today.day))) {
                  displayDate = "Today";
                } else if (parsedDate.isAtSameMomentAs(DateTime(yesterday.year, yesterday.month, yesterday.day))) {
                  displayDate = "Yesterday";
                } else {
                  displayDate = dateFormat.format(parsedDate); // Format the date with abbreviated month
                }

                return Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(5.0),
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
                            padding: const EdgeInsets.all(3.0),
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
                                          fontSize: 16,
                                          fontWeight: FontWeight.w600,
                                          fontFamily: 'Roboto',
                                        ),
                                      ),
                                      subtitle: Text('Time: ${detail['time']}'),
                                    ),
                                    if (detailIndex != details.length - 1)
                                      const Divider(
                                        height: 2,
                                        thickness: 0.5,
                                        indent: 12,
                                        endIndent: 12,
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
            );
          } else {
            return const Center(child: Text('No history available'));
          }
        },
      ),
    );
  }
}
