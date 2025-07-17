# ai_engine/feature_engineer.py
import pandas as pd
import numpy as np
from datetime import datetime

class FeatureEngineer:
    def __init__(self):
        # Initialize with some known malicious IPs
        self.malicious_ips = [
            '192.168.1.1',
            '10.0.0.15',
            '172.16.0.39'
        ]
        self.high_risk_ports = [22, 3389, 445, 1433]
        
    def preprocess_data(self, raw_data):
        """Convert raw logs into ML-ready features with consistent column names"""
        features = []
        
        for _, row in raw_data.iterrows():
            if row['source'] == 'network_traffic':
                features.append(self._process_network(row))
            elif row['source'] == 'email_server':
                features.append(self._process_email(row))
            elif row['source'] == 'payment_systems':
                features.append(self._process_payment(row))
            elif row['source'] == 'endpoint_devices':
                features.append(self._process_endpoint(row))
            elif row['source'] == 'threat_intel_feeds':
                features.append(self._process_threat_intel(row))
        
        # Define consistent feature names for all data types
        feature_columns = [
            'hour_of_day',
            'is_high_risk_port',
            'ip_reputation',
            'bytes_per_second',
            'is_internal',
            'action_denied',
            'has_attachment',
            'is_external',
            'suspicious_subject',
            'large_amount',
            'foreign_currency',
            'transaction_failed',
            'failed_access',
            'unusual_hour',
            'known_malicious',
            'phishing_related'
        ]
        
        # Create DataFrame with all columns (missing features will be NaN)
        features_df = pd.DataFrame(features)
        
        # Ensure all expected columns exist (fill missing with 0)
        for col in feature_columns:
            if col not in features_df.columns:
                features_df[col] = 0
                
        # Return only the columns we need for our models
        model_features = [
            'hour_of_day',
            'is_high_risk_port',
            'ip_reputation',
            'bytes_per_second',
            'is_internal',
            'action_denied'
        ]
        
        return features_df[model_features]

    def _process_network(self, row):
        """Extract network traffic features"""
        return {
            'hour_of_day': row['timestamp'].hour,
            'is_high_risk_port': 1 if row['port'] in self.high_risk_ports else 0,
            'ip_reputation': 1 if row['src_ip'] in self.malicious_ips else 0,
            'bytes_per_second': row['bytes'] / row['duration'] if row['duration'] > 0 else 0,
            'is_internal': 1 if row['dst_ip'].startswith('10.0.') else 0,
            'action_denied': 1 if row['action'] == 'DENY' else 0
        }
    
    def _process_email(self, row):
        """Extract email features"""
        return {
            'hour_of_day': row['timestamp'].hour,
            'has_attachment': 1 if row['has_attachment'] else 0,
            'is_external': 1 if row['is_external'] else 0,
            'suspicious_subject': 1 if 'urgent' in row['subject'].lower() else 0
        }
    
    def _process_payment(self, row):
        """Extract payment system features"""
        return {
            'hour_of_day': row['timestamp'].hour,
            'large_amount': 1 if row['amount'] > 100000 else 0,
            'foreign_currency': 1 if row['currency'] != 'USD' else 0,
            'transaction_failed': 1 if row['status'] == 'REJECTED' else 0
        }
    
    def _process_endpoint(self, row):
        """Extract endpoint device features"""
        return {
            'hour_of_day': row['timestamp'].hour,
            'failed_access': 1 if not row['success'] else 0,
            'unusual_hour': 1 if row['timestamp'].hour < 6 or row['timestamp'].hour > 20 else 0
        }
    
    def _process_threat_intel(self, row):
        """Extract threat intelligence features"""
        return {
            'hour_of_day': row['timestamp'].hour,
            'known_malicious': 1 if 'malicious' in row['value'] else 0,
            'phishing_related': 1 if row['threat_type'] == 'phishing' else 0
        }