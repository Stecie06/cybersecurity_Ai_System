import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/threat_service.dart';
import '../widgets/alert_card.dart';

class AlertsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final threatService = Provider.of<ThreatService>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: Text('Critical Alerts'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () => threatService.refresh(),
          ),
        ],
      ),
      body: FutureBuilder(
        future: threatService.getCriticalAlerts(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }
          
          final alerts = snapshot.data ?? [];
          
          if (alerts.isEmpty) {
            return Center(child: Text('No critical alerts found'));
          }
          
          return ListView.builder(
            itemCount: alerts.length,
            itemBuilder: (ctx, index) => AlertCard(alert: alerts[index]),
          );
        },
      ),
    );
  }
}