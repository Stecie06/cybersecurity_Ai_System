import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/threat_report.dart';
import '../services/threat_service.dart';
import '../widgets/threat_card.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Threat Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => context.read<ThreatService>().refreshThreats(),
          ),
        ],
      ),
      body: _buildThreatsList(),
    );
  }

  Widget _buildThreatsList() {
    return Consumer<ThreatService>(
      builder: (context, service, _) {
        return StreamBuilder<List<ThreatReport>>(
          stream: service.threatsStream,
          builder: (context, snapshot) {
            if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            }
            
            if (!snapshot.hasData) {
              return const Center(child: CircularProgressIndicator());
            }
            
            final threats = snapshot.data!;
            return Column(
              children: [
                _buildStatsRow(threats),
                Expanded(child: _buildThreatsListView(threats)),
              ],
            );
          },
        );
      },
    );
  }

  Widget _buildThreatsListView(List<ThreatReport> threats) {
    return ListView.builder(
      itemCount: threats.length,
      itemBuilder: (context, index) => ThreatCard(threat: threats[index]),
    );
  }

  Widget _buildStatsRow(List<ThreatReport> threats) {
    final criticalCount = threats.where((t) => t.severity == 'CRITICAL').length;
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatItem('Total', threats.length, Colors.blue),
          _buildStatItem('Critical', criticalCount, Colors.red),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, int count, Color color) {
    return Column(
      children: [
        Text(
          count.toString(),
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(label),
      ],
    );
  }
}