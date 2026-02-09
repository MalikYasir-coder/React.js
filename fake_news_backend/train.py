"""
Model Training Script
Train the fake news detection model on a dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

from models.news_classifier import NewsClassifier
from utils.text_cleaner import TextCleaner


def train_model(csv_file):
    """
    Train the fake news detection model
    
    Expected CSV format:
    - Column 'text' or 'news': The news article text
    - Column 'label' or 'is_fake': 0 for real news, 1 for fake news
    """
    
    print("Loading data...")
    df = pd.read_csv(csv_file)
    
    # Handle different column names
    text_column = None
    label_column = None
    
    for col in df.columns:
        if col.lower() in ['text', 'news', 'article', 'content']:
            text_column = col
        if col.lower() in ['label', 'is_fake', 'fake', 'target']:
            label_column = col
    
    if text_column is None or label_column is None:
        raise ValueError("CSV must contain 'text' and 'label' columns (or similar)")
    
    # Prepare data
    X = df[text_column].values
    y = df[label_column].values
    
    print(f"Total samples: {len(X)}")
    print(f"Fake news: {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
    print(f"Real news: {len(y) - sum(y)} ({(len(y) - sum(y))/len(y)*100:.1f}%)")
    
    # Clean text
    cleaner = TextCleaner()
    print("\nCleaning text...")
    X_cleaned = [cleaner.clean_text(text) for text in X]
    
    # Split data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_cleaned, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    print("Training model...")
    classifier = NewsClassifier()
    classifier.train_model(X_train, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred = [classifier.predict(text) for text in X_test]
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"True Negatives:  {cm[0,0]}")
    print(f"False Positives: {cm[0,1]}")
    print(f"False Negatives: {cm[1,0]}")
    print(f"True Positives:  {cm[1,1]}")
    
    # Save model
    print("\nSaving model...")
    classifier.save_model()
    
    print("Training complete!")


def evaluate_on_custom_data(csv_file):
    """Evaluate pre-trained model on custom data"""
    
    print("Loading model...")
    classifier = NewsClassifier()
    classifier.load_model()
    
    print("Loading data...")
    df = pd.read_csv(csv_file)
    
    # Handle column names
    text_column = None
    label_column = None
    
    for col in df.columns:
        if col.lower() in ['text', 'news', 'article', 'content']:
            text_column = col
        if col.lower() in ['label', 'is_fake', 'fake', 'target']:
            label_column = col
    
    if text_column is None:
        raise ValueError("CSV must contain a text column")
    
    X = df[text_column].values
    y = df[label_column].values if label_column else None
    
    cleaner = TextCleaner()
    X_cleaned = [cleaner.clean_text(text) for text in X]
    
    # Make predictions
    predictions = [classifier.predict(text) for text in X_cleaned]
    confidences = [classifier.get_confidence(text) for text in X_cleaned]
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'original_text': X,
        'prediction': ['FAKE' if p == 1 else 'REAL' for p in predictions],
        'confidence': confidences
    })
    
    if y is not None:
        results_df['actual'] = ['FAKE' if label == 1 else 'REAL' for label in y]
        accuracy = accuracy_score(y, predictions)
        print(f"\nAccuracy on custom dataset: {accuracy:.4f}")
    
    # Save results
    results_df.to_csv('predictions.csv', index=False)
    print("Results saved to predictions.csv")
    print("\nSample predictions:")
    print(results_df.head(10))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train fake news detection model')
    parser.add_argument('--train', type=str, help='Path to CSV file for training')
    parser.add_argument('--evaluate', type=str, help='Path to CSV file for evaluation')
    
    args = parser.parse_args()
    
    if args.train:
        train_model(args.train)
    elif args.evaluate:
        evaluate_on_custom_data(args.evaluate)
    else:
        print("Usage:")
        print("  Training:   python train.py --train path/to/data.csv")
        print("  Evaluation: python train.py --evaluate path/to/data.csv")
        print("\nCSV should have 'text' and 'label' columns")
