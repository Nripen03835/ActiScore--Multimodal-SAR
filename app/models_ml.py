"""
Model loading and prediction utilities for ActiScore
"""

import os
import pickle
import json
import random
import numpy as np
from config import Config

def load_mock_fer_model():
    """Load mock FER model"""
    try:
        with open(Config.FER_MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        print(f"FER model not found at {Config.FER_MODEL_PATH}")
        return None

def load_mock_ser_model():
    """Load mock SER model"""
    try:
        with open(Config.SER_MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        print(f"SER model not found at {Config.SER_MODEL_PATH}")
        return None

def load_mock_fusion_model():
    """Load mock fusion model"""
    try:
        with open(Config.FUSION_MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        print(f"Fusion model not found at {Config.FUSION_MODEL_PATH}")
        return None

def load_feature_scaler():
    """Load feature scaler"""
    try:
        with open(Config.FEATURE_SCALER_PATH, 'rb') as f:
            scaler_data = pickle.load(f)
        return scaler_data
    except FileNotFoundError:
        print(f"Feature scaler not found at {Config.FEATURE_SCALER_PATH}")
        return None

def mock_fer_predict(face_image):
    """
    Mock FER prediction function
    
    Args:
        face_image: Input face image (48x48x1)
    
    Returns:
        tuple: (emotion, confidence)
    """
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    emotion = random.choice(emotions)
    confidence = random.uniform(0.5, 0.95)
    return emotion, confidence

def mock_ser_predict(audio_features):
    """
    Mock SER prediction function
    
    Args:
        audio_features: Audio feature vector
    
    Returns:
        tuple: (emotion, confidence)
    """
    emotions = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']
    emotion = random.choice(emotions)
    confidence = random.uniform(0.4, 0.9)
    return emotion, confidence

def mock_fusion_predict(fer_result, ser_result):
    """
    Mock fusion prediction function
    
    Args:
        fer_result: FER prediction (emotion, confidence)
        ser_result: SER prediction (emotion, confidence)
    
    Returns:
        tuple: (fused_emotion, fused_confidence)
    """
    fer_emotion, fer_conf = fer_result
    ser_emotion, ser_conf = ser_result
    
    # Simple weighted fusion (FER gets higher weight)
    if fer_conf > ser_conf:
        fused_emotion = fer_emotion
        fused_confidence = fer_conf * 0.8 + ser_conf * 0.2
    else:
        fused_emotion = ser_emotion
        fused_confidence = fer_conf * 0.2 + ser_conf * 0.8
    
    return fused_emotion, fused_confidence

def extract_mock_audio_features(audio_file_path):
    """
    Extract mock audio features for demonstration
    
    Args:
        audio_file_path: Path to audio file
    
    Returns:
        np.array: Mock feature vector
    """
    # Return random features for demonstration
    return np.random.rand(47)  # 47 features as defined in SER model

def process_video_emotions_mock(video_path, user_id, video_id):
    """
    Process video for emotion analysis using mock models
    
    Args:
        video_path: Path to video file
        user_id: User ID
        video_id: Video ID
    
    Returns:
        dict: Processing results
    """
    from app.models import FERResult, SERResult, FusionResult
    from app import db
    from datetime import datetime
    
    results = {
        'fer_results': [],
        'ser_results': [],
        'fusion_results': []
    }
    
    try:
        # Simulate processing frames (every 0.5 seconds)
        for i in range(10):
            timestamp = i * 0.5
            
            # FER prediction
            fer_emotion, fer_confidence = mock_fer_predict(None)
            
            # SER prediction (simulate audio segment)
            ser_emotion, ser_confidence = mock_ser_predict(None)
            
            # Fusion prediction
            fused_emotion, fused_confidence = mock_fusion_predict(
                (fer_emotion, fer_confidence),
                (ser_emotion, ser_confidence)
            )
            
            # Save FER result
            fer_result = FERResult(
                user_id=user_id,
                video_id=video_id,
                frame_ts=timestamp,
                face_bbox=json.dumps({'x': 100, 'y': 100, 'w': 200, 'h': 200}),
                emotion=fer_emotion,
                confidence=fer_confidence
            )
            db.session.add(fer_result)
            results['fer_results'].append({
                'timestamp': timestamp,
                'emotion': fer_emotion,
                'confidence': fer_confidence
            })
            
            # Save SER result (every 1 second)
            if i % 2 == 0:
                ser_result = SERResult(
                    user_id=user_id,
                    audio_id=video_id,
                    ts=timestamp,
                    emotion=ser_emotion,
                    confidence=ser_confidence
                )
                db.session.add(ser_result)
                results['ser_results'].append({
                    'timestamp': timestamp,
                    'emotion': ser_emotion,
                    'confidence': ser_confidence
                })
            
            # Save fusion result (every 2 seconds)
            if i % 4 == 0:
                fusion_result = FusionResult(
                    user_id=user_id,
                    video_id=video_id,
                    timestamp=timestamp,
                    fer_emotion=fer_emotion,
                    ser_emotion=ser_emotion,
                    fused_label=fused_emotion,
                    score=fused_confidence
                )
                db.session.add(fusion_result)
                results['fusion_results'].append({
                    'timestamp': timestamp,
                    'fused_emotion': fused_emotion,
                    'score': fused_confidence,
                    'fer_emotion': fer_emotion,
                    'ser_emotion': ser_emotion
                })
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error processing video emotions: {str(e)}")
        raise
    
    return results

def get_model_info():
    """Get information about loaded models"""
    fer_model = load_mock_fer_model()
    ser_model = load_mock_ser_model()
    fusion_model = load_mock_fusion_model()
    
    info = {
        'fer_model': {
            'loaded': fer_model is not None,
            'type': fer_model.get('model_type', 'unknown') if fer_model else None,
            'accuracy': fer_model.get('accuracy', 0) if fer_model else 0,
            'emotions': fer_model.get('emotions', []) if fer_model else []
        },
        'ser_model': {
            'loaded': ser_model is not None,
            'type': ser_model.get('model_type', 'unknown') if ser_model else None,
            'accuracy': ser_model.get('accuracy', 0) if ser_model else 0,
            'emotions': ser_model.get('emotions', []) if ser_model else []
        },
        'fusion_model': {
            'loaded': fusion_model is not None,
            'type': fusion_model.get('model_type', 'unknown') if fusion_model else None,
            'accuracy': fusion_model.get('accuracy', 0) if fusion_model else 0,
            'emotions': fusion_model.get('emotions', []) if fusion_model else []
        }
    }
    
    return info

# Initialize models on module import
print("Initializing ActiScore models...")
MODEL_INFO = get_model_info()
print(f"Model info: {MODEL_INFO}")