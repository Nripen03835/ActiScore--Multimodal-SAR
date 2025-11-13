#!/usr/bin/env python3
"""
Speech Emotion Recognition (SER) Model Training Script
Trains models using audio features for emotion recognition from speech.
"""

import os
import pandas as pd
import numpy as np
import librosa
import soundfile as sf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

def extract_audio_features(audio_path, sr=22050, duration=3):
    """Extract audio features from audio file"""
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=sr, duration=duration)
        
        # Extract features
        features = {}
        
        # MFCC features (13 coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_std'] = np.std(mfccs, axis=1)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_mean'] = np.mean(chroma, axis=1)
        features['chroma_std'] = np.std(chroma, axis=1)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_rolloff_std'] = np.std(spectral_rolloff)
        
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
        features['zero_crossing_rate_mean'] = np.mean(zero_crossing_rate)
        features['zero_crossing_rate_std'] = np.std(zero_crossing_rate)
        
        # Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features['tempo'] = tempo
        
        # RMS energy
        rms = librosa.feature.rms(y=y)
        features['rms_mean'] = np.mean(rms)
        features['rms_std'] = np.std(rms)
        
        # Flatten all features into a single array
        feature_vector = []
        for key, value in features.items():
            if isinstance(value, np.ndarray):
                feature_vector.extend(value)
            else:
                feature_vector.append(value)
        
        return np.array(feature_vector)
        
    except Exception as e:
        print(f"Error processing {audio_path}: {str(e)}")
        return None

def load_ser_dataset(dataset_path):
    """Load and process SER dataset"""
    print(f"Loading SER dataset from {dataset_path}")
    
    # Get all audio files
    audio_files = []
    emotions = []
    
    # Walk through the dataset directory
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                
                # Extract emotion from filename (RAVDESS format)
                # Format: 03-01-01-01-01-01-01.wav
                parts = file.split('-')
                if len(parts) >= 4:
                    emotion_code = int(parts[2])
                    emotion = get_emotion_from_code(emotion_code)
                    if emotion:
                        audio_files.append(file_path)
                        emotions.append(emotion)
    
    print(f"Found {len(audio_files)} audio files")
    print(f"Emotion distribution: {pd.Series(emotions).value_counts()}")
    
    return audio_files, emotions

def get_emotion_from_code(code):
    """Map emotion codes to emotion names (RAVDESS format)"""
    emotion_map = {
        1: 'neutral',
        2: 'calm',
        3: 'happy',
        4: 'sad',
        5: 'angry',
        6: 'fearful',
        7: 'disgust',
        8: 'surprised'
    }
    return emotion_map.get(code)

def extract_features_from_dataset(audio_files, emotions):
    """Extract features from all audio files"""
    print("Extracting features from audio files...")
    
    features = []
    labels = []
    
    for audio_file, emotion in tqdm(zip(audio_files, emotions), total=len(audio_files)):
        feature_vector = extract_audio_features(audio_file)
        if feature_vector is not None:
            features.append(feature_vector)
            labels.append(emotion)
    
    features = np.array(features)
    labels = np.array(labels)
    
    print(f"Extracted features from {len(features)} audio files")
    print(f"Feature vector size: {features.shape[1]}")
    
    return features, labels

def train_ser_models(X_train, y_train, X_val, y_val):
    """Train multiple SER models"""
    print("Training SER models...")
    
    models = {}
    
    # 1. Support Vector Machine
    print("Training SVM...")
    svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
    svm_model.fit(X_train, y_train)
    models['svm'] = svm_model
    
    # 2. Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    models['random_forest'] = rf_model
    
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

def evaluate_best_model(model, X_test, y_test, label_encoder, model_name):
    """Evaluate the best performing model"""
    print(f"Evaluating {model_name} model...")
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_encoder.classes_, 
                yticklabels=label_encoder.classes_)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(f'ser_confusion_matrix_{model_name}.png')
    plt.close()
    
    return accuracy, y_pred

def save_models(models, scaler, label_encoder, feature_names, save_dir='models'):
    """Save trained models and preprocessing objects"""
    os.makedirs(save_dir, exist_ok=True)
    
    # Save models
    for name, model in models.items():
        model_path = os.path.join(save_dir, f'ser_{name}_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Saved {name} model to {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(save_dir, 'feature_scaler_efficient.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Saved scaler to {scaler_path}")
    
    # Save label encoder
    encoder_path = os.path.join(save_dir, 'ser_label_encoder.pkl')
    with open(encoder_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    print(f"Saved label encoder to {encoder_path}")
    
    # Save feature names
    features_path = os.path.join(save_dir, 'ser_feature_names.pkl')
    with open(features_path, 'wb') as f:
        pickle.dump(feature_names, f)
    print(f"Saved feature names to {features_path}")

def plot_model_comparison(results):
    """Plot model comparison"""
    models = list(results.keys())
    train_accuracies = [results[model]['train_accuracy'] for model in models]
    val_accuracies = [results[model]['val_accuracy'] for model in models]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, train_accuracies, width, label='Training Accuracy', alpha=0.8)
    bars2 = ax.bar(x + width/2, val_accuracies, width, label='Validation Accuracy', alpha=0.8)
    
    ax.set_xlabel('Models')
    ax.set_ylabel('Accuracy')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
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
    plt.savefig('ser_model_comparison.png')
    plt.close()

def main():
    """Main training function"""
    # Configuration
    dataset_path = 'Dataset/SER_Dataset/Audio_Song_Actors_01-24'
    save_dir = 'models'
    
    print("Starting SER Model Training...")
    print("=" * 50)
    
    # Load dataset
    audio_files, emotions = load_ser_dataset(dataset_path)
    
    if len(audio_files) == 0:
        print("No audio files found. Please check the dataset path.")
        return
    
    # Extract features
    features, labels = extract_features_from_dataset(audio_files, emotions)
    
    if len(features) == 0:
        print("No features extracted. Please check the audio files.")
        return
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        features, labels, test_size=0.3, random_state=42, stratify=labels
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
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_val_encoded = label_encoder.transform(y_val)
    y_test_encoded = label_encoder.transform(y_test)
    
    print(f"Emotion classes: {label_encoder.classes_}")
    
    # Train models
    models, results = train_ser_models(X_train_scaled, y_train_encoded, 
                                     X_val_scaled, y_val_encoded)
    
    # Plot model comparison
    plot_model_comparison(results)
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['val_accuracy'])
    best_model = models[best_model_name]
    
    print(f"\nBest model: {best_model_name}")
    print(f"Validation accuracy: {results[best_model_name]['val_accuracy']:.4f}")
    
    # Evaluate best model on test set
    test_accuracy, y_pred = evaluate_best_model(
        best_model, X_test_scaled, y_test_encoded, label_encoder, best_model_name
    )
    
    # Save models and preprocessing objects
    feature_names = [
        'mfcc_mean_1', 'mfcc_mean_2', 'mfcc_mean_3', 'mfcc_mean_4', 'mfcc_mean_5',
        'mfcc_mean_6', 'mfcc_mean_7', 'mfcc_mean_8', 'mfcc_mean_9', 'mfcc_mean_10',
        'mfcc_mean_11', 'mfcc_mean_12', 'mfcc_mean_13',
        'mfcc_std_1', 'mfcc_std_2', 'mfcc_std_3', 'mfcc_std_4', 'mfcc_std_5',
        'mfcc_std_6', 'mfcc_std_7', 'mfcc_std_8', 'mfcc_std_9', 'mfcc_std_10',
        'mfcc_std_11', 'mfcc_std_12', 'mfcc_std_13',
        'chroma_mean_1', 'chroma_mean_2', 'chroma_mean_3', 'chroma_mean_4', 
        'chroma_mean_5', 'chroma_mean_6', 'chroma_mean_7', 'chroma_mean_8',
        'chroma_mean_9', 'chroma_mean_10', 'chroma_mean_11', 'chroma_mean_12',
        'chroma_std_1', 'chroma_std_2', 'chroma_std_3', 'chroma_std_4',
        'chroma_std_5', 'chroma_std_6', 'chroma_std_7', 'chroma_std_8',
        'chroma_std_9', 'chroma_std_10', 'chroma_std_11', 'chroma_std_12',
        'spectral_centroid_mean', 'spectral_centroid_std',
        'spectral_rolloff_mean', 'spectral_rolloff_std',
        'zero_crossing_rate_mean', 'zero_crossing_rate_std',
        'tempo', 'rms_mean', 'rms_std'
    ]
    
    save_models(models, scaler, label_encoder, feature_names, save_dir)
    
    print("\n" + "=" * 50)
    print("Training completed!")
    print(f"Best model: {best_model_name}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Models saved to: {save_dir}")
    print("=" * 50)

if __name__ == '__main__':
    main()