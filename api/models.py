from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ThreatType(str, Enum):
    PHISHING = "Phishing Attempt"
    MALWARE = "Malware Activity"
    FRAUD = "Financial Fraud"
    INSIDER = "Insider Threat"
    UNAUTHORIZED_ACCESS = "Unauthorized Access"
    DDOS = "DDoS Attempt"

class ThreatReport(BaseModel):
    timestamp: datetime
    threat_level: ThreatLevel
    threat_type: ThreatType
    source: str
    indicators: str
    description: Optional[str] = None

class AlertNotification(BaseModel):
    alert_id: str
    timestamp: datetime
    threat_reports: List[ThreatReport]
    recommended_actions: List[str]

class SystemHealth(BaseModel):
    status: str
    last_scan: datetime
    threats_detected: int
    avg_response_time: float