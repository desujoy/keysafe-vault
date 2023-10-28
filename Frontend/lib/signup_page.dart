import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class SignupPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sign Up'),
      ),
      body: SignupForm(),
    );
  }
}

class SignupForm extends StatefulWidget {
  @override
  _SignupFormState createState() => _SignupFormState();
}

class _SignupFormState extends State<SignupForm> {
  final _formKey = GlobalKey<FormState>();
  String _username = '';
  String _email = '';
  String _password = '';

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextFormField(
              decoration: InputDecoration(
                hintText: 'Enter your username',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter your username';
                }
                return null;
              },
              onChanged: (value) {
                setState(() {
                  _username = value;
                });
              },
            ),
            TextFormField(
              decoration: InputDecoration(
                hintText: 'Enter your email',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter your email';
                }
                if (!value.contains('@')) {
                  return 'Please enter a valid email address';
                }
                return null;
              },
              onChanged: (value) {
                setState(() {
                  _email = value;
                });
              },
            ),
            TextFormField(
              decoration: InputDecoration(
                hintText: 'Enter your password',
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter your password';
                }
                return null;
              },
              onChanged: (value) {
                setState(() {
                  _password = value;
                });
              },
              obscureText: true,
            ),
            ElevatedButton(
              onPressed: () async {
                if (_formKey.currentState!.validate()) {
                  var map = new Map<String, dynamic>();
                  map['username'] = _username;
                  map['email'] = _email;
                  map['password'] = _password;

                  final response = await http.post(
                    Uri.parse('http://localhost:3000/auth/register'),
                    body: map,
                  );

                  if (response.statusCode == 200) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('User created successfully'),
                      ),
                    );
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Failed to create user. Please try again.'),
                      ),
                    );
                  }
                }
              },
              child: Text('Create User'),
            ),
          ],
        ),
      ),
    );
  }
}
