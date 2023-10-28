import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CardsPage extends StatefulWidget {
  final String username;

  CardsPage({required this.username});

  @override
  _CardsPageState createState() => _CardsPageState();
}

class _CardsPageState extends State<CardsPage> {
  List<Map<String, dynamic>> cards = [];

  final TextEditingController _cardNameController = TextEditingController();
  final TextEditingController _cardNumberController = TextEditingController();
  final TextEditingController _cardTypeController = TextEditingController();
  final TextEditingController _expiryDateController = TextEditingController();
  final TextEditingController _cvvController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchCards();
  }

  Future<void> _fetchCards() async {
    final username = widget.username;
    final url = 'http://localhost:3000/data/cards?username=$username';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final List<dynamic> dataList = json.decode(response.body);
        cards.clear();
        print(dataList);

        for (var data in dataList) {
          if (true) {
            final cardName = data['name'].toString();
            final cardNumber = data['card_number'].toString();
            final cardType = data['card_type'].toString();
            final expiryDate = data['card_exp'].toString();
            final cvv = data['card_cvv'].toString();
            cards.add({
              'cardName': cardName,
              'cardNumber': cardNumber,
              'cardType': cardType,
              'expiryDate': expiryDate,
              'cvv': cvv,
            });
          }
        }
        setState(() {});
      } else {
        print('Failed to fetch cards. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  Future<void> _saveCard() async {
    final cardName = _cardNameController.text;
    final cardNumber = _cardNumberController.text;
    final cardType = _cardTypeController.text;
    final expiryDate = _expiryDateController.text;
    final cvv = _cvvController.text;
    final loggedInUser = widget.username;

    final url = 'http://localhost:3000/data/cards';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'cardName': cardName,
          'cardNumber': cardNumber,
          'cardType': cardType,
          'expiryDate': expiryDate,
          'cvv': cvv,
          'loggedInUser': loggedInUser,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          print('Card saved successfully');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Card Saved')),
          );
          // Clear input fields
          _cardNameController.clear();
          _cardNumberController.clear();
          _cardTypeController.clear();
          _expiryDateController.clear();
          _cvvController.clear();
          // Fetch the updated list of cards
          _fetchCards();
        } else {
          print('Failed to save card. Server response: ${data['message']}');
        }
      } else {
        print('Failed to save card. Error: ${response.statusCode}');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  void _openAddCardDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Save Card Details'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _cardNameController,
                decoration: InputDecoration(
                  labelText: 'Card Name',
                ),
              ),
              TextField(
                controller: _cardNumberController,
                decoration: InputDecoration(
                  labelText: 'Card Number',
                ),
              ),
              TextField(
                controller: _cardTypeController,
                decoration: InputDecoration(
                  labelText: 'Card Type',
                ),
              ),
              TextField(
                controller: _expiryDateController,
                decoration: InputDecoration(
                  labelText: 'Expiry Date',
                ),
              ),
              TextField(
                controller: _cvvController,
                decoration: InputDecoration(
                  labelText: 'CVV',
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
                _saveCard();
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
        title: Text('Cards'),
      ),
      body: ListView.builder(
        itemCount: cards.length,
        itemBuilder: (context, index) {
          final cardData = cards[index];
          final cardName = cardData['cardName'];
          final cardNumber = cardData['cardNumber'];
          final cardType = cardData['cardType'];
          final expiryDate = cardData['expiryDate'];
          final cvv = cardData['cvv'];

          return Card(
            margin: EdgeInsets.all(8.0),
            child: ListTile(
              title: Text('Card Name: $cardName'),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Card Number: $cardNumber'),
                  Text('Card Type: $cardType'),
                  Text('Expiry Date: $expiryDate'),
                  Text('CVV: $cvv'),
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
        onPressed: _openAddCardDialog,
        child: Icon(Icons.add),
      ),
    );
  }
}
