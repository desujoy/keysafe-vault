import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class FilesPage extends StatefulWidget {
  final String username;

  FilesPage({
    required this.username,
  });

  @override
  _FilesPageState createState() => _FilesPageState();
}

class _FilesPageState extends State<FilesPage> {
  List<PlatformFile> files = [];

  Future<void> _uploadFile() async {
    final dio = Dio();
    final url = 'http://localhost:3000/data/files';

    final result = await FilePicker.platform.pickFiles(allowMultiple: true);
    if (result != null) {
      setState(() {
        files.addAll(result.files);
      });
    }
    
    for (final selectedFile in result!.files) {
      final formData = FormData.fromMap({
        'name': selectedFile.name,
        'loggedInUser': widget.username,
        'file': MultipartFile.fromBytes(selectedFile.bytes!),
      });

      try {
        await dio.post(url, data: formData);
        print('File uploaded successfully: ${selectedFile.name}');
      } catch (e) {
        print('Error uploading file: $e');
      }
    }
  }

  Future<void> _downloadFile(PlatformFile file) async {
    final saveDirectory = await FilePicker.platform.getDirectoryPath();
    if (saveDirectory != null) {
      final savePath = '$saveDirectory/${file.name}';

      final dio = Dio();
      final url = 'http://localhost:3000/data/files/${file.name}'; // Update with your actual download URL

      try {
        await dio.download(url, savePath);
        print('File downloaded successfully: $savePath');
      } catch (e) {
        print('Error downloading file: $e');
      }
    }
  }

  void _deleteFile(PlatformFile file) {
    setState(() {
      files.removeWhere((f) => f.name == file.name);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('File Upload and Management'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
            onPressed: _uploadFile,
            child: Text('Upload File'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: files.length,
              itemBuilder: (context, index) {
                final file = files[index];
                return ListTile(
                  title: Text(file.name),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.download),
                        onPressed: () => _downloadFile(file),
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () => _deleteFile(file),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
