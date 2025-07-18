import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/threat_report.dart';

class ThreatService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  final FirebaseAuth _auth = FirebaseAuth.instance;

  Stream<List<ThreatReport>> get threatsStream {
    return _firestore
        .collection('threats')
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => ThreatReport.fromJson(doc.data()))
            .toList());
  }

  Future<List<ThreatReport>> getAllThreats() async {
    try {
      final snapshot = await _firestore
          .collection('threats')
          .orderBy('timestamp', descending: true)
          .get();
      return snapshot.docs.map((doc) => ThreatReport.fromJson(doc.data())).toList();
    } catch (e) {
      throw Exception('Failed to load threats: $e');
    }
  }

  Future<List<ThreatReport>> getCriticalAlerts() async {
    final snapshot = await _firestore
        .collection('threats')
        .where('severity', isEqualTo: 'CRITICAL')
        .orderBy('timestamp', descending: true)
        .get();
    return snapshot.docs.map((doc) => ThreatReport.fromJson(doc.data())).toList();
  }

  Stream<List<ThreatReport>> getCriticalAlertsStream() {
    return _firestore
        .collection('threats')
        .where('severity', isEqualTo: 'CRITICAL')
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => ThreatReport.fromJson(doc.data()))
            .toList());
  }

  Future<void> refreshThreats() async {
    await _firestore.collection('threats').get();
  }

  Future<void> addThreat(ThreatReport threat) async {
    await _firestore.collection('threats').add(threat.toJson());
  }
}