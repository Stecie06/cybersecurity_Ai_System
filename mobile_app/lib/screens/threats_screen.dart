import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/threat_service.dart';
import '../widgets/threat_card.dart';

class ThreatsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final threatService = Provider.of<ThreatService>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: Text('All Threats'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () => threatService.refresh(),
          ),
        ],
      ),
      body: FutureBuilder(
        future: threatService.getAllThreats(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }
          
          final threats = snapshot.data ?? [];
          
          return ListView.builder(
            itemCount: threats.length,
            itemBuilder: (ctx, index) => ThreatCard(threat: threats[index]),
          );
        },
      ),
    );
  }
}