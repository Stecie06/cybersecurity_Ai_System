import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/threat_report.dart';
import '../services/threat_service.dart';
import '../widgets/threat_card.dart';
import 'alerts_screen.dart';
import 'threats_screen.dart';
import 'settings_screen.dart';

class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Threat Dashboard'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () => context.read<ThreatService>().fetchThreats(),
          ),
        ],
      ),
      drawer: _buildDrawer(context),
      body: StreamBuilder<List<ThreatReport>>(
        stream: context.watch<ThreatService>().threatsStream,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          
          if (!snapshot.hasData) {
            return Center(child: CircularProgressIndicator());
          }
          
          final threats = snapshot.data!;
          return Column(
            children: [
              _buildStatsRow(threats),
              Expanded(
                child: ListView.builder(
                  itemCount: threats.length,
                  itemBuilder: (context, index) => ThreatCard(threat: threats[index]),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildDrawer(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColor,
            ),
            child: Text(
              'Security Menu',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
              ),
            ),
          ),
          ListTile(
            leading: Icon(Icons.warning),
            title: Text('Alerts'),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => AlertsScreen()),
              );
            },
          ),
          ListTile(
            leading: Icon(Icons.list),
            title: Text('All Threats'),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => ThreatsScreen()),
              );
            },
          ),
          ListTile(
            leading: Icon(Icons.settings),
            title: Text('Settings'),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SettingsScreen()),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildStatsRow(List<ThreatReport> threats) {
    final criticalCount = threats.where((t) => t.severity == 'CRITICAL').length;
    final highCount = threats.where((t) => t.severity == 'HIGH').length;
    
    return Padding(
      padding: EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatItem('Total', threats.length, Colors.blue),
          _buildStatItem('Critical', criticalCount, Colors.red),
          _buildStatItem('High', highCount, Colors.orange),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, int count, Color color) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          count.toString(),
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(
          label,
          style: TextStyle(fontSize: 14),
        ),
      ],
    );
  }
}