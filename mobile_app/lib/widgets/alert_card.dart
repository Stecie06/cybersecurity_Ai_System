import 'package:flutter/material.dart';

class AlertCard extends StatelessWidget {
  final Map<String, dynamic> alert;

  const AlertCard({required this.alert});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.red[50],
      margin: EdgeInsets.symmetric(vertical: 5, horizontal: 10),
      child: ListTile(
        leading: Icon(Icons.warning, color: Colors.red),
        title: Text(
          alert['threat_type'] ?? 'Critical Alert',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(alert['indicators'] ?? 'Immediate action required'),
        trailing: Text(alert['timestamp']?.split(' ')[0] ?? ''),
      ),
    );
  }
}