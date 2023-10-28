import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class NotesPage extends StatefulWidget {
  final String username;

  NotesPage({required this.username});

  @override
  _NotesPageState createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  List<Map<String, dynamic>> notes = [];

  final TextEditingController _notesNamecontroller = TextEditingController();
  final TextEditingController _contentController = TextEditingController();


  @override
  void initState() {
    super.initState();
    _fetchNotes();
  }

  Future<void> _fetchNotes() async {
    final username = widget.username;
    final url = 'http://localhost:3000/data/notes?username=$username';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final List<dynamic> dataList = json.decode(response.body);
        notes.clear();
        print(dataList);

        for (var data in dataList) {
          if (true) {
            final noteName = data['name'].toString();
            final noteContent = data['content'].toString();

            notes.add({
              'noteName': noteName,
              'noteContent': noteContent,

            });
          }
        }
        setState(() {});
      } else {
        print('Failed to fetch notes. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  Future<void> _saveNotes() async {
    final noteName = _notesNamecontroller.text;
    final noteContent = _contentController.text;
    final loggedInUser = widget.username;

    final url = 'http://localhost:3000/data/cards';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'noteName': noteName,
          'noteContent': noteContent,
          'loggedInUser': loggedInUser,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          print('Note saved successfully');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Note Saved')),
          );

          _notesNamecontroller.clear();
          _contentController.clear();
          _fetchNotes();
        } else {
          print('Failed to save note. Server response: ${data['message']}');
        }
      } else {
        print('Failed to save note. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  void _openAddNoteDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Save Notes'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _notesNamecontroller,
                decoration: InputDecoration(
                  labelText: 'Name',
                ),
              ),
              TextField(
                controller: _contentController,
                decoration: InputDecoration(
                  labelText: 'Content',
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                _saveNotes();
              },
              child: Text('Save'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Notes'),
      ),
      body: ListView.builder(
        itemCount: notes.length,
        itemBuilder: (context, index) {
          final noteData = notes[index];
          final noteName = noteData['notesName'];
          final noteContent = noteData['noteContent'];

          return Card(
            margin: EdgeInsets.all(8.0),
            child: ListTile(
              title: Text('Note Name: $noteName'),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Content: $noteContent'),

                ],
              ),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: Icon(Icons.edit),
                    onPressed: () {
                      // Implement the edit functionality
                    },
                  ),
                  IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () {
                      // Implement the delete functionality
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openAddNoteDialog,
        child: Icon(Icons.add),
      ),
    );
  }
}
