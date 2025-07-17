# ai_engine/data_collector.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import pytz

class DataCollector:
    def __init__(self):
        self.sources = [
            'network_traffic', 'email_server', 'payment_systems',
            'endpoint_devices', 'threat_intel_feeds'
        ]
        
    def simulate_real_time_data(self, num_entries=100):
        """Simulate real-time security logs from various sources"""
        data = []
        now = datetime.now(pytz.utc)
        
        for _ in range(num_entries):
            source = random.choice(self.sources)
            timestamp = now - timedelta(minutes=random.randint(0, 60))
            
            if source == 'network_traffic':
                entry = self._generate_network_traffic(timestamp)
            elif source == 'email_server':
                entry = self._generate_email_data(timestamp)
            elif source == 'payment_systems':
                entry = self._generate_payment_data(timestamp)
            elif source == 'endpoint_devices':
                entry = self._generate_endpoint_data(timestamp)
            else:
                entry = self._generate_threat_intel(timestamp)
                
            data.append(entry)
            
        return pd.DataFrame(data)
    
    def _generate_network_traffic(self, timestamp):
        """Simulate network traffic logs"""
        return {
            'timestamp': timestamp,
            'source': 'network_traffic',
            'src_ip': f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            'dst_ip': f"10.0.{random.randint(1,254)}.{random.randint(1,254)}",
            'port': random.choice([80, 443, 22, 3389, 445]),
            'bytes': random.randint(100, 100000),
            'duration': random.uniform(0.1, 60.0),
            'protocol': random.choice(['TCP', 'UDP']),
            'action': random.choice(['ALLOW', 'DENY'])
        }
    
    def _generate_email_data(self, timestamp):
        """Simulate email logs"""
        return {
            'timestamp': timestamp,
            'source': 'email_server',
            'from': f"user{random.randint(1,100)}@example.com",
            'to': f"bankstaff{random.randint(1,50)}@centralbank.org",
            'subject': random.choice(['Account Update', 'Urgent Action Required', 'Payment Notification']),
            'has_attachment': random.choice([True, False]),
            'is_external': random.choice([True, False])
        }
    
    def _generate_payment_data(self, timestamp):
        """Simulate payment system logs"""
        return {
            'timestamp': timestamp,
            'source': 'payment_systems',
            'from_account': f"ACCT{random.randint(100000,999999)}",
            'to_account': f"ACCT{random.randint(100000,999999)}",
            'amount': random.uniform(10, 1000000),
            'currency': random.choice(['USD', 'EUR', 'GBP']),
            'status': random.choice(['COMPLETED', 'PENDING', 'REJECTED'])
        }
    
    def _generate_endpoint_data(self, timestamp):
        """Simulate endpoint device logs"""
        return {
            'timestamp': timestamp,
            'source': 'endpoint_devices',
            'device_id': f"DEV{random.randint(1000,9999)}",
            'event_type': random.choice(['login', 'file_access', 'process_start']),
            'user': f"user{random.randint(1,500)}",
            'success': random.choice([True, False])
        }
    
    def _generate_threat_intel(self, timestamp):
        """Simulate threat intelligence feeds"""
        return {
            'timestamp': timestamp,
            'source': 'threat_intel_feeds',
            'indicator': random.choice(['IP', 'Domain', 'URL']),
            'value': f"{random.choice(['malicious', 'suspicious'])}-{random.randint(1,1000)}.com",
            'threat_type': random.choice(['phishing', 'malware', 'botnet'])
        }