# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import sys
import random

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.data_collector import DataCollector
from ai_engine.feature_engineer import FeatureEngineer

def train_anomaly_model():
    """Train isolation forest for anomaly detection"""
    print("Generating training data...")
    collector = DataCollector()
    engineer = FeatureEngineer()
    
    # Generate normal data (low threat)
    normal_data = collector.simulate_real_time_data(1000)
    normal_features = engineer.preprocess_data(normal_data)
    
    # Generate attack data (high threat)
    print("Generating attack data...")
    attack_data = collector.simulate_real_time_data(200)
    # Modify some features to simulate attacks
    for i in range(len(attack_data)):
        if random.random() > 0.7:
            if 'port' in attack_data.columns:
                attack_data.loc[i, 'port'] = random.choice([22, 3389, 445])  # High-risk ports
            if 'src_ip' in attack_data.columns:
                attack_data.loc[i, 'src_ip'] = f"192.168.{random.randint(1,254)}.1"  # Suspicious IP
    
    attack_features = engineer.preprocess_data(attack_data)
    
    # Label data
    X = pd.concat([normal_features, attack_features])
    y = np.array([0] * len(normal_features) + [1] * len(attack_features))
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training anomaly detection model...")
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    model.fit(X_train)
    
    # Evaluate
    preds = model.predict(X_test)
    print("\nAnomaly Detection Performance:")
    print(classification_report(y_test, [1 if x == -1 else 0 for x in preds]))
    
    # Save model
    os.makedirs('ml_models', exist_ok=True)
    joblib.dump(model, 'ml_models/anomaly_model.pkl')
    print("Saved model to ml_models/anomaly_model.pkl")

if __name__ == "__main__":
    train_anomaly_model()