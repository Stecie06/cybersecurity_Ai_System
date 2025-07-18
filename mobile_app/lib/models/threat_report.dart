// lib/models/threat_report.dart
class ThreatReport {
  final String id;
  final String threatType;
  final String severity;
  final String sourceIp;
  final DateTime timestamp;
  final Map<String, dynamic> details;

  ThreatReport({
    required this.id,
    required this.threatType,
    required this.severity,
    required this.sourceIp,
    required this.timestamp,
    required this.details,
  });

  factory ThreatReport.fromJson(Map<String, dynamic> json) {
    return ThreatReport(
      id: json['id'] ?? '',
      threatType: json['threat_type'] ?? 'Unknown',
      severity: json['severity'] ?? 'MEDIUM',
      sourceIp: json['source_ip'] ?? '0.0.0.0',
      timestamp: DateTime.parse(json['timestamp']),
      details: json['details'] ?? {},
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'threat_type': threatType,
    'severity': severity,
    'source_ip': sourceIp,
    'timestamp': timestamp.toIso8601String(),
    'details': details,
  };
}