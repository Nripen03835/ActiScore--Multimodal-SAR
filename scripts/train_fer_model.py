#!/usr/bin/env python3
"""
Facial Emotion Recognition (FER) Model Training Script
Trains a CNN model using the FER2013 dataset for emotion recognition.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

def load_fer_data(dataset_path):
    """Load FER2013 dataset from CSV file"""
    print(f"Loading FER dataset from {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Emotion distribution:\n{df['emotion'].value_counts()}")
    return df

def preprocess_fer_data(df):
    """Preprocess FER data"""
    print("Preprocessing FER data...")
    
    # Convert pixel strings to arrays
    pixels = df['pixels'].tolist()
    faces = []
    
    for pixel_sequence in pixels:
        # Convert string of space-separated integers to numpy array
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.asarray(face).reshape(48, 48)
        faces.append(face)
    
    faces = np.asarray(faces)
    faces = faces.reshape(-1, 48, 48, 1)
    faces = faces.astype('float32') / 255.0  # Normalize to [0, 1]
    
    # Encode emotions
    emotions = df['emotion'].values
    label_encoder = LabelEncoder()
    emotion_labels = label_encoder.fit_transform(emotions)
    
    # Convert to categorical
    num_classes = len(label_encoder.classes_)
    emotion_categorical = tf.keras.utils.to_categorical(emotion_labels, num_classes)
    
    print(f"Preprocessed data shape: {faces.shape}")
    print(f"Number of emotion classes: {num_classes}")
    print(f"Emotion labels: {label_encoder.classes_}")
    
    return faces, emotion_categorical, label_encoder

def create_fer_model(input_shape, num_classes):
    """Create CNN model for FER"""
    print("Creating FER CNN model...")
    
    model = Sequential([
        # First convolutional block
        Conv2D(64, (3, 3), activation='relu', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Second convolutional block
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Third convolutional block
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Fully connected layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_fer_model(model, X_train, y_train, X_val, y_val, model_save_path):
    """Train the FER model"""
    print("Training FER model...")
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(model_save_path, monitor='val_accuracy', save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001)
    ]
    
    # Train model
    history = model.fit(
        X_train, y_train,
        batch_size=32,
        epochs=50,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def evaluate_model(model, X_test, y_test, label_encoder, emotion_names):
    """Evaluate the trained model"""
    print("Evaluating model...")
    
    # Get predictions
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    # Classification report
    print("Classification Report:")
    print(classification_report(y_true_classes, y_pred_classes, 
                              target_names=emotion_names))
    
    # Confusion matrix
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=emotion_names, yticklabels=emotion_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('fer_confusion_matrix.png')
    plt.close()
    
    return y_pred_classes

def plot_training_history(history, save_path='fer_training_history.png'):
    """Plot training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    """Main training function"""
    # Configuration
    dataset_path = 'Dataset/FER_Dataset/fer2013.csv'
    model_save_path = 'models/fer_model.h5'
    label_encoder_path = 'models/fer_label_encoder.pkl'
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Load data
    df = load_fer_data(dataset_path)
    
    # Preprocess data
    faces, emotion_categorical, label_encoder = preprocess_fer_data(df)
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        faces, emotion_categorical, test_size=0.2, random_state=42, stratify=np.argmax(emotion_categorical, axis=1)
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=np.argmax(y_temp, axis=1)
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Create model
    input_shape = (48, 48, 1)
    num_classes = emotion_categorical.shape[1]
    model = create_fer_model(input_shape, num_classes)
    
    # Print model summary
    model.summary()
    
    # Train model
    history = train_fer_model(model, X_train, y_train, X_val, y_val, model_save_path)
    
    # Plot training history
    plot_training_history(history)
    
    # Save label encoder
    with open(label_encoder_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # Evaluate on test set
    emotion_names = label_encoder.classes_
    y_pred_classes = evaluate_model(model, X_test, y_test, label_encoder, emotion_names)
    
    # Save final model
    model.save(model_save_path)
    
    print(f"\nTraining completed!")
    print(f"Model saved to: {model_save_path}")
    print(f"Label encoder saved to: {label_encoder_path}")
    print(f"Training history saved to: fer_training_history.png")
    print(f"Confusion matrix saved to: fer_confusion_matrix.png")

if __name__ == '__main__':
    main()