import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/threat_report.dart';
import '../services/threat_service.dart';
import '../widgets/alert_card.dart';

class ThreatsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final threatService = Provider.of<ThreatService>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('All Threats'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => ThreatsScreen()),
            ),
          ),
        ],
      ),
      body: FutureBuilder<List<ThreatReport>>(
        future: threatService.getAllThreats(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (snapshot.hasError) {
            return Center(
              child: Text(
                'Error loading threats: ${snapshot.error}',
                style: const TextStyle(color: Colors.red),
              ),
            );
          }
          
          final threats = snapshot.data ?? [];
          
          if (threats.isEmpty) {
            return const Center(child: Text('No threats found'));
          }
          
          return ListView.builder(
            itemCount: threats.length,
            itemBuilder: (ctx, index) => AlertCard(alert: threats[index]),
          );
        },
      ),
    );
  }
}