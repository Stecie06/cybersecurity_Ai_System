// lib/widgets/threat_card.dart
import 'package:flutter/material.dart';
import '../models/threat_report.dart';

class ThreatCard extends StatelessWidget {
  final ThreatReport threat;
  
  const ThreatCard({required this.threat, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.all(8),
      child: ListTile(
        leading: Icon(Icons.warning, color: _getThreatColor(threat.severity)),
        title: Text(threat.threatType),
        subtitle: Text('${threat.sourceIp} - ${_formatTime(threat.timestamp)}'),
        trailing: Icon(Icons.chevron_right),
        onTap: () {
          // Add navigation to threat details if needed
        },
      ),
    );
  }

  Color _getThreatColor(String severity) {
    switch (severity.toUpperCase()) {
      case 'CRITICAL': return Colors.red;
      case 'HIGH': return Colors.orange;
      case 'MEDIUM': return Colors.yellow;
      case 'LOW': return Colors.blue;
      default: return Colors.grey;
    }
  }

  String _formatTime(DateTime timestamp) {
    return '${timestamp.hour}:${timestamp.minute.toString().padLeft(2, '0')}';
  }
}