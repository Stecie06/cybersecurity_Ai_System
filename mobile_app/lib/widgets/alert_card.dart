import 'package:flutter/material.dart';
import '../models/threat_report.dart';

class AlertCard extends StatelessWidget {
  final ThreatReport alert;
  
  const AlertCard({required this.alert, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      elevation: 3,
      child: ListTile(
        leading: Icon(
          Icons.warning,
          color: _getThreatColor(alert.severity),
        ),
        title: Text(
          alert.threatType,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: _getThreatColor(alert.severity),
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Severity: ${alert.severity}'),
            Text('Time: ${_formatTime(alert.timestamp)}'),
          ],
        ),
        trailing: const Icon(Icons.chevron_right),
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