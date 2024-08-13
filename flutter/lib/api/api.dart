import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart';

class ApiService {
  static Future<http.Response> uploadImage(File image, String name) async {
    var uri = Uri.parse("http://192.168.80.65:5000/extract");
    var request = http.MultipartRequest('POST', uri);

    // Determine the mime type of the file
    String? mimeType = lookupMimeType(image.path);
    if (mimeType == null) {
      throw Exception("Could not determine mime type of the image.");
    }
    var mimeTypeData = mimeType.split('/');

    request.files.add(
      await http.MultipartFile.fromPath(
        'images',
        image.path,
        contentType: MediaType(mimeTypeData[0], mimeTypeData[1]),
      ),
    );

    // Add name field
    request.fields['name'] = name;
    request.fields['username']="varun";

    return await http.Response.fromStream(await request.send());
  }
}
