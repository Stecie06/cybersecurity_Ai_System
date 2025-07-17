# ai_engine/threat_classifier.py
from enum import Enum
import pandas as pd
from datetime import datetime
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ThreatType(Enum):
    PHISHING = "Phishing Attempt"
    MALWARE = "Malware Activity"
    FRAUD = "Financial Fraud"
    INSIDER = "Insider Threat"
    UNAUTHORIZED_ACCESS = "Unauthorized Access"
    DDOS = "DDoS Attempt"
    SUSPICIOUS_TRAFFIC = "Suspicious Network Traffic"

class ThreatClassifier:
    def __init__(self):
        self.port_threat_mapping = {
            22: "SSH Brute Force Attempt",
            3389: "RDP Exploit Attempt",
            445: "SMB Exploit Attempt",
            1433: "SQL Server Exploit Attempt"
        }
        
        self.keyword_triggers = {
            "login": "Suspicious Login Activity",
            "transfer": "Unusual Fund Transfer",
            "payment": "Suspicious Payment"
        }

    def _safe_get(self, log_entry: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Safely get value from log entry with type checking"""
        value = log_entry.get(key, default)
        
        # Handle pandas NA/null values
        if pd.isna(value):
            return default
            
        return value

    def _determine_threat_type(self, log_entry: Dict[str, Any]) -> ThreatType:
        """Determine the specific threat type with robust type checking"""
        source = self._safe_get(log_entry, 'source', 'unknown')
        
        if source == 'email_server':
            return ThreatType.PHISHING
        elif source == 'payment_systems':
            return ThreatType.FRAUD
        elif source == 'network_traffic':
            port = self._safe_get(log_entry, 'port')
            if port in self.port_threat_mapping:
                return ThreatType.MALWARE
            return ThreatType.SUSPICIOUS_TRAFFIC
        elif source == 'endpoint_devices':
            success = self._safe_get(log_entry, 'success', True)
            if not success:
                return ThreatType.UNAUTHORIZED_ACCESS
        return ThreatType.INSIDER

    def _extract_indicators(self, log_entry: Dict[str, Any]) -> str:
        """Safely extract indicators with type checking"""
        indicators = []
        
        # IP Addresses
        src_ip = self._safe_get(log_entry, 'src_ip')
        if src_ip and isinstance(src_ip, str):
            indicators.append(f"Source IP: {src_ip}")
            
        dst_ip = self._safe_get(log_entry, 'dst_ip')
        if dst_ip and isinstance(dst_ip, str):
            indicators.append(f"Destination IP: {dst_ip}")
        
        # Ports
        port = self._safe_get(log_entry, 'port')
        if port and isinstance(port, (int, float)):
            indicators.append(f"Port: {int(port)}")
            if int(port) in self.port_threat_mapping:
                indicators.append(self.port_threat_mapping[int(port)])
        
        # Amounts
        amount = self._safe_get(log_entry, 'amount')
        if amount and isinstance(amount, (int, float)):
            indicators.append(f"Amount: {amount:.2f}")
        
        # Subjects (with type checking)
        subject = self._safe_get(log_entry, 'subject')
        if subject and isinstance(subject, str):
            if 'urgent' in subject.lower():
                indicators.append("Urgent subject line")
            if any(kw in subject.lower() for kw in self.keyword_triggers):
                indicators.append("Suspicious keywords")
        
        return ", ".join(indicators) if indicators else "No specific indicators"

    def classify(self, detection_results: list, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Classify threats with comprehensive error handling"""
        classified = []
        
        for i, threat_level in enumerate(detection_results):
            if threat_level in ['HIGH', 'CRITICAL']:
                try:
                    log_entry = raw_data.iloc[i].to_dict()
                    threat_type = self._determine_threat_type(log_entry)
                    indicators = self._extract_indicators(log_entry)
                    
                    timestamp = self._safe_get(log_entry, 'timestamp')
                    if not timestamp:
                        timestamp = datetime.now().isoformat()
                    elif not isinstance(timestamp, str):
                        timestamp = str(timestamp)
                    
                    classified.append({
                        'timestamp': timestamp,
                        'source': self._safe_get(log_entry, 'source', 'unknown'),
                        'threat_level': threat_level,
                        'threat_type': threat_type.value,
                        'indicators': indicators
                    })
                    
                except Exception as e:
                    logger.error(f"Error classifying threat at index {i}: {str(e)}", exc_info=True)
                    continue
        
        if classified:
            return pd.DataFrame(classified)[['timestamp', 'source', 'threat_level', 'threat_type', 'indicators']]
        return pd.DataFrame()

    def save_to_csv(self, classified_threats: pd.DataFrame, filepath: str = "logs/central_reports.csv") -> None:
        """Save threats to CSV with robust file handling"""
        if not classified_threats.empty:
            try:
                import os
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                # Write with header if file doesn't exist
                header = not os.path.exists(filepath)
                classified_threats.to_csv(filepath, mode='a', header=header, index=False)
                logger.info(f"Saved {len(classified_threats)} threats to {filepath}")
            except Exception as e:
                logger.error(f"Failed to save threats: {str(e)}", exc_info=True)