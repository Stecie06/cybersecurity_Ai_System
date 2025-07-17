# run_monitor.py
import time
import logging
from ai_engine.data_collector import DataCollector
from ai_engine.feature_engineer import FeatureEngineer
from ai_engine.detector import ThreatDetector
from ai_engine.threat_classifier import ThreatClassifier
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_threats():
    """Continuously monitor for threats"""
    collector = DataCollector()
    engineer = FeatureEngineer()
    detector = ThreatDetector()
    classifier = ThreatClassifier()

    while True:
        try:
            # Step 1: Collect data
            raw_data = collector.simulate_real_time_data(50)  # Simulate 50 new log entries
            
            # Step 2: Extract features
            features = engineer.preprocess_data(raw_data)
            
            # Step 3: Detect threats
            threat_levels = detector.detect_threats(features)
            
            # Step 4: Classify threats
            classified_threats = classifier.classify(threat_levels, raw_data)
            
            if not classified_threats.empty:
                # Save to CSV (or database in production)
                classified_threats.to_csv("logs/central_reports.csv", mode='a', header=False)
                logger.info(f"Detected {len(classified_threats)} new threats")
            
            time.sleep(60)  # Check every 60 seconds
            
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_threats()