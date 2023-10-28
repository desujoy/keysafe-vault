import 'package:flutter/material.dart';
import 'package:login2/cards.dart';
import 'package:login2/notes.dart';
import 'package:login2/passwords.dart';
import 'package:login2/files.dart';

class NavDrawer extends StatelessWidget {
  final String username;
  NavDrawer({required this.username});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            child: Text(
              'Security = KeySafe',
              style: TextStyle(color: Colors.white, fontSize: 25),
            ),
            decoration: BoxDecoration(
                color: Color.fromARGB(255, 10, 10, 11),  
                image: DecorationImage(
                    fit: BoxFit.fill,
                    image: AssetImage('C:/Users/pragy/Downloads/project main.jpg'))),
          ),
          ListTile(
            leading: Icon(Icons.people),
            title: Text('Profile'),
            onTap: () => {},
          ),
          ListTile(
            leading: Icon(Icons.verified_user),
              title: Text('Passwords'),
                onTap: () {
            Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => PasswordsPage(username: username))
            );
          },
         ),
          ListTile(
            leading: Icon(Icons.card_giftcard_outlined),
              title: Text('Cards'),
                onTap: ()  {
            Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => CardsPage(username: username))
            );
          },
        ),
          ListTile(
            leading: Icon(Icons.notes),
            title: Text('Secure Notes'),
            onTap: () {
            Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => NotesPage(username: username))
            );   
            },
          ),
          ListTile(
            leading: Icon(Icons.file_copy_sharp),
            title: Text('Files'),
            onTap: ()  {
              Navigator.of(context).push(
              MaterialPageRoute(builder: (context) => FilesPage(username: username))    
            );
          },
        ),
          ListTile(
            leading: Icon(Icons.exit_to_app),
            title: Text('Logout'),
            onTap: () => {Navigator.of(context).pop()},
          ),
        ],
      ),
    );
  }
}

class PersonalizedPage extends StatelessWidget {
    final String username; 
    
  PersonalizedPage({required this.username}); 
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Hello $username'),
      ),
      drawer: NavDrawer(username: username),
      body: Center(
        child: Text('Welcome to KeySafe'),
      ),
    );
  }
}