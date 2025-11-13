#!/usr/bin/env python3
"""
Fusion Model Training Script
Combines FER and SER predictions for improved emotion recognition.
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def create_fusion_dataset(fer_predictions, ser_predictions, true_labels):
    """Create fusion dataset by combining FER and SER predictions"""
    print("Creating fusion dataset...")
    
    # Ensure predictions are in the same format
    if len(fer_predictions) != len(ser_predictions) or len(fer_predictions) != len(true_labels):
        raise ValueError("FER, SER, and true labels must have the same length")
    
    # Create feature matrix
    # Features: [fer_confidence, ser_confidence, fer_prediction, ser_prediction]
    fusion_features = []
    
    for i in range(len(fer_predictions)):
        fer_pred = fer_predictions[i]
        ser_pred = ser_predictions[i]
        
        # Create feature vector
        features = [
            fer_pred['confidence'],
            ser_pred['confidence'],
            fer_pred['emotion_class'],
            ser_pred['emotion_class'],
            fer_pred.get('emotion_score', 0.0),
            ser_pred.get('emotion_score', 0.0)
        ]
        
        fusion_features.append(features)
    
    return np.array(fusion_features)

def train_fusion_models(X_train, y_train, X_val, y_val, emotion_labels):
    """Train multiple fusion models"""
    print("Training fusion models...")
    
    models = {}
    
    # 1. Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train, y_train)
    models['logistic_regression'] = lr_model
    
    # 2. Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    models['random_forest'] = rf_model
    
    # 3. Gradient Boosting
    print("Training Gradient Boosting...")
    gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    models['gradient_boosting'] = gb_model
    
    # Evaluate models
    results = {}
    for name, model in models.items():
        train_accuracy = model.score(X_train, y_train)
        val_accuracy = model.score(X_val, y_val)
        
        results[name] = {
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'model': model
        }
        
        print(f"{name} - Train: {train_accuracy:.4f}, Val: {val_accuracy:.4f}")
    
    return models, results

def evaluate_fusion_model(model, X_test, y_test, emotion_labels, model_name):
    """Evaluate fusion model"""
    print(f"Evaluating {model_name} fusion model...")
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=emotion_labels))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=emotion_labels, 
                yticklabels=emotion_labels)
    plt.title(f'Fusion Model Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(f'fusion_confusion_matrix_{model_name}.png')
    plt.close()
    
    return accuracy, y_pred

def plot_fusion_comparison(results):
    """Plot fusion model comparison"""
    models = list(results.keys())
    train_accuracies = [results[model]['train_accuracy'] for model in models]
    val_accuracies = [results[model]['val_accuracy'] for model in models]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, train_accuracies, width, label='Training Accuracy', alpha=0.8)
    bars2 = ax.bar(x + width/2, val_accuracies, width, label='Validation Accuracy', alpha=0.8)
    
    ax.set_xlabel('Fusion Models')
    ax.set_ylabel('Accuracy')
    ax.set_title('Fusion Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace('_', ' ').title() for m in models])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('fusion_model_comparison.png')
    plt.close()

def create_ensemble_predictions(models, X_test):
    """Create ensemble predictions from multiple models"""
    predictions = []
    
    for model in models.values():
        pred = model.predict(X_test)
        predictions.append(pred)
    
    # Majority voting
    ensemble_pred = []
    for i in range(len(predictions[0])):
        votes = [pred[i] for pred in predictions]
        # Get most common prediction
        from collections import Counter
        vote_count = Counter(votes)
        ensemble_pred.append(vote_count.most_common(1)[0][0])
    
    return np.array(ensemble_pred)

def save_fusion_models(models, scaler, emotion_labels, save_dir='models'):
    """Save fusion models and preprocessing objects"""
    os.makedirs(save_dir, exist_ok=True)
    
    # Save models
    for name, model in models.items():
        model_path = os.path.join(save_dir, f'fusion_{name}_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Saved {name} fusion model to {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(save_dir, 'fusion_scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Saved scaler to {scaler_path}")
    
    # Save emotion labels
    labels_path = os.path.join(save_dir, 'fusion_emotion_labels.pkl')
    with open(labels_path, 'wb') as f:
        pickle.dump(emotion_labels, f)
    print(f"Saved emotion labels to {labels_path}")

def simulate_fer_ser_predictions():
    """Simulate FER and SER predictions for demonstration"""
    print("Simulating FER and SER predictions...")
    
    # Emotion classes
    emotions = ['neutral', 'happy', 'sad', 'angry', 'surprised', 'fearful', 'disgust']
    
    # Simulate predictions for 100 samples
    n_samples = 100
    
    fer_predictions = []
    ser_predictions = []
    true_labels = []
    
    for i in range(n_samples):
        # True emotion (random)
        true_emotion = np.random.choice(emotions)
        true_labels.append(true_emotion)
        
        # FER prediction (with some noise)
        if np.random.random() < 0.7:  # 70% accuracy
            fer_emotion = true_emotion
        else:
            fer_emotion = np.random.choice(emotions)
        
        fer_predictions.append({
            'emotion_class': emotions.index(fer_emotion),
            'confidence': np.random.uniform(0.6, 0.95),
            'emotion_score': np.random.uniform(0.5, 1.0)
        })
        
        # SER prediction (with some noise)
        if np.random.random() < 0.65:  # 65% accuracy
            ser_emotion = true_emotion
        else:
            ser_emotion = np.random.choice(emotions)
        
        ser_predictions.append({
            'emotion_class': emotions.index(ser_emotion),
            'confidence': np.random.uniform(0.5, 0.9),
            'emotion_score': np.random.uniform(0.4, 0.9)
        })
    
    return fer_predictions, ser_predictions, true_labels, emotions

def main():
    """Main training function"""
    print("Starting Fusion Model Training...")
    print("=" * 50)
    
    # For demonstration, simulate FER and SER predictions
    # In real implementation, load actual predictions from trained models
    fer_predictions, ser_predictions, true_labels, emotion_labels = simulate_fer_ser_predictions()
    
    # Create fusion dataset
    fusion_features = create_fusion_dataset(fer_predictions, ser_predictions, true_labels)
    
    # Encode labels
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(true_labels)
    
    print(f"Fusion feature shape: {fusion_features.shape}")
    print(f"Number of samples: {len(true_labels)}")
    print(f"Emotion classes: {label_encoder.classes_}")
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        fusion_features, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Validation set: {len(X_val)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Feature scaling
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Train fusion models
    models, results = train_fusion_models(
        X_train_scaled, y_train, X_val_scaled, y_val, label_encoder.classes_
    )
    
    # Plot model comparison
    plot_fusion_comparison(results)
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['val_accuracy'])
    best_model = models[best_model_name]
    
    print(f"\nBest fusion model: {best_model_name}")
    print(f"Validation accuracy: {results[best_model_name]['val_accuracy']:.4f}")
    
    # Evaluate best model on test set
    test_accuracy, y_pred = evaluate_fusion_model(
        best_model, X_test_scaled, y_test, label_encoder.classes_, best_model_name
    )
    
    # Test ensemble approach
    ensemble_pred = create_ensemble_predictions(models, X_test_scaled)
    ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
    print(f"\nEnsemble accuracy: {ensemble_accuracy:.4f}")
    
    # Save models
    save_fusion_models(models, scaler, label_encoder.classes_.tolist())
    
    print("\n" + "=" * 50)
    print("Fusion training completed!")
    print(f"Best model: {best_model_name}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Ensemble accuracy: {ensemble_accuracy:.4f}")
    print("=" * 50)

if __name__ == '__main__':
    main()