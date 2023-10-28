import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PasswordsPage extends StatefulWidget {
  final String username;

  PasswordsPage({required this.username});

  @override
  _PasswordsPageState createState() => _PasswordsPageState();
}

class _PasswordsPageState extends State<PasswordsPage> {
  List<Map<String, dynamic>> passwords = [];

  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _usernameEmailController = TextEditingController();
  final TextEditingController _websiteAppController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchPasswords();
  }

  Future<void> _fetchPasswords() async {
    final username = widget.username;
    final url = 'http://localhost:3000/data/pass?username=$username';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final List<dynamic> dataList = json.decode(response.body);

        setState(() {
          passwords = List<Map<String, dynamic>>.from(dataList);
        });
      } else {
        print('Failed to fetch passwords. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  Future<void> _savePassword() async {
    final name = _nameController.text;
    final password = _passwordController.text;
    final usernameEmail = _usernameEmailController.text;
    final websiteApp = _websiteAppController.text;
    final loggedInUser = widget.username;

    final url = 'http://localhost:3000/data/pass';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'name': name,
          'password': password,
          'username': usernameEmail,
          'website': websiteApp,
          'loggedInUser': loggedInUser,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          print('Password saved successfully');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Password saved')),
          );
          _fetchPasswords();
        } else {
          print('Failed to save password. Server response: ${data['message']}');
        }
      } else {
        print('Failed to save password. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  void _openAddPasswordsDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Save Passwords'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Name',
                ),
              ),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Passwords',
                ),
              ),
              TextField(
                controller: _usernameEmailController,
                decoration: InputDecoration(
                  labelText: 'Username/Email',
                ),
              ),
              TextField(
                controller: _websiteAppController,
                decoration: InputDecoration(
                  labelText: 'Website/App',
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
                _savePassword();
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
        title: Text('Passwords'),
      ),
      body: ListView.builder(
        itemCount: passwords.length,
        itemBuilder: (context, index) {
          final passwordData = passwords[index];
          final passwordName = passwordData['name'];
          final passwordValue = passwordData['password'];
          final usernameEmail = passwordData['username'];
          final websiteApp = passwordData['website'];
          final passwordId = passwordData['id'];

          return Card(
            margin: EdgeInsets.all(8.0),
            child: ListTile(
              title: Text('Name: $passwordName'),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Password: $passwordValue'),
                  Text('Username/Email: $usernameEmail'),
                  Text('Website/App: $websiteApp'),
                ],
              ),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: Icon(Icons.edit),
                    onPressed: () {
                      _editPassword(passwordId.toString());
                    },
                  ),
                  IconButton(
                    icon: Icon(Icons.delete),
                    onPressed: () {
                      _deletePassword(passwordId.toString());
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openAddPasswordsDialog,
        child: Icon(Icons.add),
      ),
    );
  }

  Future<void> _editPassword(String passwordId) async {
    final passwordData = passwords.firstWhere((element) => element['id'] == int.parse(passwordId));

    _nameController.text = passwordData['name'];
    _passwordController.text = passwordData['password'];
    _usernameEmailController.text = passwordData['username'];
    _websiteAppController.text = passwordData['website'];

    final updatedPasswordData = {
      'id': passwordId,
      'name': _nameController.text,
      'password': _passwordController.text,
      'username': _usernameEmailController.text,
      'website': _websiteAppController.text,
      'loggedInUser': widget.username,
    };

    final url = 'http://localhost:3000/data/pass/$passwordId';

    try {
      final response = await http.put(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(updatedPasswordData),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          print('Password edited successfully');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Password edited')),
          );
          _fetchPasswords();
        } else {
          print('Failed to edit password. Server response: ${data['message']}');
        }
      } else {
        print('Failed to edit password. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  Future<void> _deletePassword(String passwordId) async {
    final url = 'http://localhost:3000/data/pass/$passwordId';

    try {
      final response = await http.delete(Uri.parse(url));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          print('Password deleted successfully');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Password deleted')),
          );
          _fetchPasswords();
        } else {
          print('Failed to delete password. Server response: ${data['message']}');
        }
      } else {
        print('Failed to delete password. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }
}
