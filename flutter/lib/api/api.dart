import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart';
//import 'package:flutter_dotenv/flutter_dotenv.dart';

class Api {
  // Method to upload an image to the server


  static String apiUrl = 'http://192.168.31.246:5000';
  static String user= '66d36a9d42d9a5784e1a59fe';

  static Future<http.Response> uploadImage(List<File> images, String name, String relationship) async {
    var uri = Uri.parse('$apiUrl/people');
    var request = http.MultipartRequest('POST', uri);

    for (var image in images) {
      String? mimeType = lookupMimeType(image.path);
      if (mimeType == null) {
        throw Exception("Could not determine mime type of the image.");
      }
      var mimeTypeData = mimeType.split('/');

      request.files.add(
        await http.MultipartFile.fromPath(
          'images[]', // Use 'images[]' to indicate an array of files
          image.path,
          contentType: MediaType(mimeTypeData[0], mimeTypeData[1]),
        ),
      );
    }

    request.fields['name'] = name;
    request.fields['username'] = user;
    request.fields['relation'] = relationship;

    return await http.Response.fromStream(await request.send());
  }


  // Method to get profiles from the server
  static Future<http.Response> getProfiles() async {
    var uri = Uri.parse('$apiUrl/profiles/$user');
    return await http.get(uri);
  }

  // Method to get people data from the server
  static Future<List<Map<String, dynamic>>> getPeople() async {
    var uri = Uri.parse('$apiUrl/people/$user');
    var response = await http.get(uri);

    // Log the response body to see what the API returned
    print('API response: ${response.body}');

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map((item) {
        return {
          'id': item['_id'],
          'name': item['name'],
          'relationship': item['relation'],
        };
      }).toList();
    } else {
      throw Exception('Failed to load people');
    }
  }
}