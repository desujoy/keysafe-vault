import 'package:flutter/material.dart';
import 'package:login2/forgotpassword.dart';
import 'package:login2/pesonalized_page.dart';
import 'package:login2/signup_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'KeySafe Vault',
      theme: ThemeData(
        primarySwatch: Colors.grey,
      ),
      home: MyHomePage(title: 'KeySafe Vault'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final _formKey = GlobalKey<FormState>();
  String _email = '';
  String _password = '';
  String? _emailError;
  String? _passwordError;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextFormField(
                decoration: InputDecoration(
                  hintText: 'Enter your email',
                  errorText: _emailError,
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your email';
                  }
                  return null;
                },
                onChanged: (value) {
                  setState(() {
                    _email = value;
                    _emailError = null;
                  });
                },
              ),
              TextFormField(
                decoration: InputDecoration(
                  hintText: 'Enter your password',
                  errorText: _passwordError,
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
                    _passwordError = null;
                  });
                },
                obscureText: true,
              ),
              ElevatedButton(
                onPressed: () async {
                  if (_formKey.currentState!.validate()) {
                    var map = Map<String, dynamic>();
                    map['email'] = _email;
                    map['password'] = _password;

                    final response = await http.post(
                      Uri.parse('http://localhost:3000/auth/login'),
                      body: map,
                    );

                    if (response.statusCode == 200) {
                      final data = json.decode(response.body);
                      final username = data['username'];

                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => PersonalizedPage(username: username),
                        ),
                      );
                    } else {
                      setState(() {
                        _emailError = 'Invalid email or password';
                        _passwordError = 'Invalid email or password';
                      });
                    }
                  } else {
                    setState(() {
                      _emailError = 'Please enter your email';
                      _passwordError = 'Please enter your password';
                    });
                  }
                },
                child: Text('Login'),
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => SignupPage(),
                    ),
                  );
                },
                child: Text('Sign Up'),
              ),
                            ElevatedButton(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => ForgotPasswordPage(username: _email),
                    ),
                  );
                },
                child: Text('Forgot Password'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

