import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';

class ThreatService {
  final String _apiUrl = "http://YOUR_API_IP:8000"; // Replace with your API URL

  Future<String?> _getUserToken() async {
    return await FirebaseAuth.instance.currentUser?.getIdToken();
  }

  Future<List<dynamic>> getCriticalAlerts() async {
    final token = await _getUserToken();
    final response = await http.get(
      Uri.parse('$_apiUrl/alerts'),
      headers: {'Authorization': 'Bearer $token'},
    );
    return json.decode(response.body);
  }

  Future<List<dynamic>> getAllThreats() async {
    final token = await _getUserToken();
    final response = await http.get(
      Uri.parse('$_apiUrl/threat-reports'),
      headers: {'Authorization': 'Bearer $token'},
    );
    return json.decode(response.body);
  }

  getCriticalThreats() {}
}