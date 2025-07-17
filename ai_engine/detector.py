import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class ThreatDetector:
    def __init__(self):
        self.models = {}
        self.feature_names = [
            'hour_of_day', 'is_high_risk_port', 'ip_reputation',
            'bytes_per_second', 'is_internal', 'action_denied'
        ]
        
        try:
            self.models['anomaly'] = joblib.load('ml_models/anomaly_model.pkl')
            logger.info("Anomaly model loaded successfully")
        except FileNotFoundError:
            logger.warning("Anomaly model not found, skipping anomaly detection")
            
        try:
            self.models['fraud'] = joblib.load('ml_models/fraud_model.pkl')
            logger.info("Fraud model loaded successfully")
        except FileNotFoundError:
            logger.warning("Fraud model not found, skipping fraud detection")
            
        self.scaler = StandardScaler()
        
    def detect_threats(self, features):
        """Run detection models on processed features"""
        if not self.models:
            return ['LOW'] * len(features)
            
        # Ensure features are in DataFrame with correct columns
        features_df = pd.DataFrame(features, columns=self.feature_names)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features_df)
        scaled_features_df = pd.DataFrame(scaled_features, columns=self.feature_names)
        
        results = []
        for i in range(len(features_df)):
            threat_level = 'LOW'
            
            # Anomaly detection
            if 'anomaly' in self.models:
                anomaly_score = self.models['anomaly'].decision_function(
                    scaled_features_df.iloc[[i]]
                )[0]
                if anomaly_score < -0.5:
                    threat_level = 'HIGH'
                elif anomaly_score < 0:
                    threat_level = 'MEDIUM'
            
            # Fraud detection
            if 'fraud' in self.models and threat_level != 'HIGH':
                fraud_prob = self.models['fraud'].predict_proba(
                    scaled_features_df.iloc[[i]]
                )[0][1]
                if fraud_prob > 0.8:
                    threat_level = 'CRITICAL'
            
            results.append(threat_level)
            
        return results