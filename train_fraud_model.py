# train_fraud_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from ai_engine.data_collector import DataCollector
from ai_engine.feature_engineer import FeatureEngineer

def train_fraud_model():
    """Train supervised fraud detection model"""
    print("Generating fraud training data...")
    collector = DataCollector()
    engineer = FeatureEngineer()
    
    # Generate normal transactions
    normal_data = collector.simulate_real_time_data(800)
    normal_data['is_fraud'] = 0  # Label normal transactions as 0
    
    # Generate fraudulent transactions
    fraud_data = collector.simulate_real_time_data(200)
    # Modify to simulate fraud patterns
    for i in range(len(fraud_data)):
        if fraud_data.loc[i, 'source'] == 'payment_systems':
            fraud_data.loc[i, 'amount'] *= 10  # Larger amounts
            fraud_data.loc[i, 'currency'] = 'USD' if random.random() > 0.5 else 'EUR'
    fraud_data['is_fraud'] = 1  # Label fraud as 1
    
    # Combine and process
    all_data = pd.concat([normal_data, fraud_data])
    features = engineer.preprocess_data(all_data)
    labels = all_data['is_fraud'].values
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.3, random_state=42
    )
    
    # Train model
    print("Training fraud detection model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print("\nFraud Detection Performance:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    import os
    os.makedirs('ml_models', exist_ok=True)
    joblib.dump(model, 'ml_models/fraud_model.pkl')
    print("Saved model to ml_models/fraud_model.pkl")

if __name__ == "__main__":
    import random
    random.seed(42)
    train_fraud_model()