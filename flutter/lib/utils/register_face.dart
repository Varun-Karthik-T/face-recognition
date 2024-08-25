import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:camera/camera.dart';
import 'dart:io';
import '../api/api.dart';

class Register extends StatefulWidget {
  const Register({super.key});

  @override
  State<Register> createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
  File? _image;
  String name = '';
  CameraController? _cameraController;
  List<CameraDescription>? _cameras;
  bool _isCameraInitialized = false;
  bool _isFrontCamera = false;
  bool _isFlashOn = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    _cameras = await availableCameras();
    if (_cameras != null && _cameras!.isNotEmpty) {
      _cameraController = CameraController(_cameras![0], ResolutionPreset.high);
      await _cameraController!.initialize();
      setState(() {
        _isCameraInitialized = true;
      });
    }
  }

  Future<void> _pickImageFromGallery() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _captureImage() async {
    if (_cameraController != null && _cameraController!.value.isInitialized) {
      final image = await _cameraController!.takePicture();
      setState(() {
        _image = File(image.path);
      });
    }
  }

  void _toggleFlash() {
    if (_cameraController != null && _cameraController!.value.isInitialized) {
      setState(() {
        _isFlashOn = !_isFlashOn;
        _cameraController!.setFlashMode(
          _isFlashOn ? FlashMode.torch : FlashMode.off,
        );
      });
    }
  }

  void _switchCamera() async {
    if (_cameras != null && _cameras!.length > 1) {
      setState(() {
        _isCameraInitialized = false;
        _isFrontCamera = !_isFrontCamera;
      });
      _cameraController = CameraController(
        _isFrontCamera ? _cameras![1] : _cameras![0],
        ResolutionPreset.high,
      );
      await _cameraController!.initialize();
      setState(() {
        _isCameraInitialized = true;
      });
    }
  }

  Future<void> _submitImage() async {
    if (_image != null && name.isNotEmpty) {
      try {
        final response = await ApiService.uploadImage(_image!, name);
        if (response.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Image uploaded successfully!')),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Failed to upload image.')),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${e.toString()}')),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No image selected or name is empty.')),
      );
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Register",
          style: TextStyle(color: Colors.white),
        ),
        iconTheme: const IconThemeData(color: Colors.white),
        backgroundColor: Colors.lightBlue[800],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickImageFromGallery,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.image, color: Colors.lightBlue[900]),
                  const SizedBox(width: 8),
                  Text(
                    'Pick from Gallery',
                    style: TextStyle(
                      color: Colors.lightBlue[900],
                    ),
                  ),
                ],
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                if (!_isCameraInitialized) {
                  await _initializeCamera();
                }
                if (_isCameraInitialized) {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => CameraScreen(
                        cameraController: _cameraController!,
                        onCapture: (file) {
                          setState(() {
                            _image = file;
                          });
                        },
                        onFlashToggle: _toggleFlash,
                        onSwitchCamera: _switchCamera,
                        isFlashOn: _isFlashOn,
                      ),
                    ),
                  );
                }
              },
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.camera_alt_rounded, color: Colors.lightBlue[900]),
                  const SizedBox(width: 8),
                  Text(
                    "Capture using Camera",
                    style: TextStyle(color: Colors.lightBlue[900]),
                  ),
                ],
              ),
            ),
            _image != null
                ? Column(
                    children: [
                      SizedBox(
                        height: 200,
                        width: 500,
                        child: Image.file(_image!),
                      ),
                      TextField(
                        cursorColor: Colors.lightBlue[900],
                        textAlign: TextAlign.center,
                        onChanged: (value) {
                          setState(() {
                            name = value;
                          });
                        },
                        decoration: const InputDecoration(
                          hintText: 'Enter person name',
                        ),
                      ),
                      ElevatedButton(
                        onPressed: _submitImage,
                        child: const Text(
                          'Submit',
                          style: TextStyle(
                            color: Colors.blue,
                          ),
                        ),
                      ),
                    ],
                  )
                : const Text(
                    'No image selected.',
                    style: TextStyle(color: Colors.grey),
                  ),
          ],
        ),
      ),
    );
  }
}

class CameraScreen extends StatelessWidget {
  final CameraController cameraController;
  final Function(File) onCapture;
  final VoidCallback onFlashToggle;
  final VoidCallback onSwitchCamera;
  final bool isFlashOn;

  const CameraScreen({super.key, 
    required this.cameraController,
    required this.onCapture,
    required this.onFlashToggle,
    required this.onSwitchCamera,
    required this.isFlashOn,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Center(child: CameraPreview(cameraController)),
          Positioned(
            bottom: 20,
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                IconButton(
                  icon: Icon(isFlashOn ? Icons.flash_on : Icons.flash_off),
                  onPressed: onFlashToggle,
                ),
                IconButton(
                  icon: const Icon(Icons.camera),
                  onPressed: () async {
                    final image = await cameraController.takePicture();
                    onCapture(File(image.path));
                    Navigator.of(context).pop();
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.switch_camera),
                  onPressed: onSwitchCamera,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
