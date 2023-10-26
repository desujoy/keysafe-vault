import 'package:flutter/material.dart';
// import 'package:google_sign_in/google_sign_in'; 
import 'package:login2/pesonalized_page.dart'; 

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

  // Future<void> _handleGoogleSignIn() async {
  //   final googleSignIn = GoogleSignIn();

  //   try {
  //     final account = await googleSignIn.signIn();

  //     if (account != null) {

  //       Navigator.of(context).push(
  //         MaterialPageRoute(
  //           builder: (context) => PersonalizedPage(),
  //         ),
  //       );
  //     } else {
  //       // User canceled Google sign-up
  //     }
  //   } catch (error) {
  //     // Handle Google sign-up error
  //     print('Google Sign-Up Error: $error');
  //   }
  // }

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
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    if (_email == 'youremail@example.com' && _password == 'yourpassword') {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => PersonalizedPage(),
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
                },
                child: Text('Sign Up'),
              ),
              // ElevatedButton(
              //   onPressed: _handleGoogleSignIn,
              //   child: Text('Sign Up with Google'),
              // ),
            ],
          ),
        ),
      ),
    );
  }
}
