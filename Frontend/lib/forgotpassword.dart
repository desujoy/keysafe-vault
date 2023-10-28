import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:dio/dio.dart';

class ForgotPasswordPage extends StatefulWidget {
  final String username;

  ForgotPasswordPage({
    required this.username,
  });

  @override
  _ForgotPasswordPageState createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  PlatformFile? file;

  Future<void> _uploadFile() async {
    final dio = Dio();
    final url = 'http://localhost:3000/data/forgotPassword'; // Replace with your actual API endpoint

    try {
      final result = await FilePicker.platform.pickFiles(allowMultiple: false);
      if (result != null) {
        setState(() {
          file = result.files.first;
        });

        final selectedFile = result.files.first;
        final formData = FormData.fromMap({
          'username': widget.username,
          'file': MultipartFile.fromBytes(selectedFile.bytes!, filename: selectedFile.name),
        });

        await dio.post(url, data: formData);
        print('File uploaded successfully: ${selectedFile.name}');
      }
    } catch (e) {
      print('Error uploading file: $e');
    }
  }

  void _deleteFile() {
    setState(() {
      file = null;
    });
  }

  // Add a method to download the uploaded file here

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Forgot Password'),
      ),
      body: Center( // Center the button vertically
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _uploadFile,
              child: Text('Upload Keygen File'),
            ),
            if (file != null)
              ListTile(
                title: Text(file!.name),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.download),
                      onPressed: () {
                        // Add code to download the file here
                      },
                    ),
                    IconButton(
                      icon: Icon(Icons.delete),
                      onPressed: _deleteFile,
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}
