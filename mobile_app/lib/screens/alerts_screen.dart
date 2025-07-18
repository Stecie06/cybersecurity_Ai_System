import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/threat_report.dart';
import '../services/threat_service.dart';
import '../widgets/alert_card.dart';

class AlertsScreen extends StatefulWidget {
  @override
  _AlertsScreenState createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  late Future<List<ThreatReport>> _alertsFuture;
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey =
      GlobalKey<RefreshIndicatorState>();

  @override
  void initState() {
    super.initState();
    _loadAlerts();
  }

  Future<void> _loadAlerts() {
    final threatService = Provider.of<ThreatService>(context, listen: false);
    setState(() {
      _alertsFuture = threatService.getCriticalAlerts();
    });
    return _alertsFuture;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Critical Alerts'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _refreshIndicatorKey.currentState?.show(),
          ),
        ],
      ),
      body: RefreshIndicator(
        key: _refreshIndicatorKey,
        onRefresh: _loadAlerts,
        child: FutureBuilder<List<ThreatReport>>(
          future: _alertsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return Center(
                child: Text(
                  'Error loading alerts: ${snapshot.error}',
                  style: const TextStyle(color: Colors.red),
                ),
              );
            }

            final alerts = snapshot.data ?? [];

            if (alerts.isEmpty) {
              return const Center(child: Text('No critical alerts found'));
            }

            return ListView.builder(
              itemCount: alerts.length,
              itemBuilder: (ctx, index) => AlertCard(alert: alerts[index]),
              addAutomaticKeepAlives: true, // Added as requested
            );
          },
        ),
      ),
    );
  }
}