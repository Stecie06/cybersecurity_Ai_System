import 'package:flutter/material.dart';

class ThreatCard extends StatelessWidget {
  final Map<String, dynamic> threat;

  const ThreatCard({required this.threat});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 5, horizontal: 10),
      child: ListTile(
        title: Text(threat['threat_type'] ?? 'Unknown Threat'),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(threat['timestamp'] ?? ''),
            SizedBox(height: 5),
            Text(threat['indicators'] ?? 'No details'),
          ],
        ),
        trailing: _getThreatIcon(threat['threat_level']),
      ),
    );
  }

  Icon _getThreatIcon(String? level) {
    switch (level?.toUpperCase()) {
      case 'CRITICAL':
        return Icon(Icons.warning, color: Colors.red);
      case 'HIGH':
        return Icon(Icons.warning_amber, color: Colors.orange);
      default:
        return Icon(Icons.info, color: Colors.blue);
    }
  }
}