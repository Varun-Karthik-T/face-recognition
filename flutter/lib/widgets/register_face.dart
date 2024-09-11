import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:camera/camera.dart';
import 'dart:io';
import '../api/api.dart';

class CameraScreen extends StatelessWidget {
  final CameraController cameraController;
  final Function(File) onCapture;
  final VoidCallback onFlashToggle;
  final VoidCallback onSwitchCamera;
  final bool isFlashOn;

  const CameraScreen({
    required this.cameraController,
    required this.onCapture,
    required this.onFlashToggle,
    required this.onSwitchCamera,
    required this.isFlashOn,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Capture Image'),
        actions: [
          IconButton(
            icon: Icon(isFlashOn ? Icons.flash_on : Icons.flash_off),
            onPressed: onFlashToggle,
          ),
          IconButton(
            icon: const Icon(Icons.switch_camera),
            onPressed: onSwitchCamera,
          ),
        ],
      ),
      body: cameraController.value.isInitialized
          ? CameraPreview(cameraController)
          : const Center(child: CircularProgressIndicator()),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final image = await cameraController.takePicture();
          onCapture(File(image.path));
          Navigator.pop(context);
        },
        child: const Icon(Icons.camera),
      ),
    );
  }
}

class Register extends StatefulWidget {
  const Register({super.key});

  @override
  State<Register> createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
  List<File> _images = [];
  String name = '';
  String relationship = '';
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
    if (_images.length >= 5) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('You can select only up to 5 images.')),
      );
      return;
    }

    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null && File(pickedFile.path).existsSync()) {
      setState(() {
        _images.add(File(pickedFile.path));
      });
    }
  }

  Future<void> _captureImage() async {
    if (_images.length >= 5) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('You can select only up to 5 images.')),
      );
      return;
    }

    if (_cameraController != null && _cameraController!.value.isInitialized) {
      final image = await _cameraController!.takePicture();
      if (File(image.path).existsSync()) {
        setState(() {
          _images.add(File(image.path));
        });
      }
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

  Future<void> _switchCamera() async {
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

  Future<void> _submitImages() async {
    if (_images.isNotEmpty && name.isNotEmpty) {
      try {

          final response = await Api.uploadImage(_images, name,relationship);
          print(response.body.toString());
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

  void _removeImage(int index) {
    setState(() {
      _images.removeAt(index);
    });
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
                  const SizedBox(width: 12),
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
                            if (_images.length < 5) {
                              _images.add(file);
                            }
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
                  const SizedBox(width: 12),
                  Text(
                    "Capture using Camera",
                    style: TextStyle(color: Colors.lightBlue[900]),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: GridView.builder(
                itemCount: _images.length,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  crossAxisSpacing: 4,
                  mainAxisSpacing: 4,
                ),
                itemBuilder: (context, index) {
                  final image = _images[index];
                  return Stack(
                    children: [
                      Image.file(
                        image,
                        fit: BoxFit.cover,
                        width: double.infinity,
                        height: double.infinity,
                      ),
                      Positioned(
                        top: 0,
                        right: 0,
                        child: IconButton(
                          icon: const Icon(Icons.close, color: Colors.red),
                          onPressed: () => _removeImage(index),
                        ),
                      ),
                    ],
                  );
                },
              ),
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
            TextField(
              cursorColor: Colors.lightBlue[900],
              textAlign: TextAlign.center,
              onChanged: (value) {
                setState(() {
                  relationship = value;
                });
              },
              decoration: const InputDecoration(
                hintText: 'Enter relationship',
              ),
            ),
            ElevatedButton(
              onPressed: _submitImages,
              child: const Text(
                'Submit',
                style: TextStyle(
                  color: Colors.blue,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}