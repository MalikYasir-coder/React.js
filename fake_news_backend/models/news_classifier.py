"""
News Classifier - Machine Learning Model
Uses TF-IDF vectorization and Naive Bayes classifier
"""

import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import numpy as np
from pathlib import Path


class NewsClassifier:
    """
    Fake News Classifier using TF-IDF and Naive Bayes
    This is a pre-trained model placeholder - in production you would train on real data
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = MultinomialNB()
        self.confidence_model = LogisticRegression()
        self.is_trained = False
        self.model_dir = Path(__file__).parent.parent / 'models' / 'saved'
        
    def load_model(self):
        """Load pre-trained model from disk"""
        try:
            model_path = self.model_dir / 'classifier.pkl'
            vectorizer_path = self.model_dir / 'vectorizer.pkl'
            
            if model_path.exists() and vectorizer_path.exists():
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                print("Model loaded successfully")
            else:
                print("No saved model found - using default model")
                self._initialize_default_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Initialize with default model (can be replaced with real training data)"""
        # Sample training data (in production, use real dataset)
        sample_news = [
            "Breaking news: Scientists discover cure for common cold",
            "Government announces new policy initiative",
            "CELEBRITY CAUGHT IN SHOCKING SCANDAL!!!",
            "SHOCKING: This one strange trick doctors don't want you to know!",
            "Stock market rises steadily after quarterly earnings",
            "Unbelievable: Woman loses 200 lbs with this ONE SECRET",
            "New research shows benefits of exercise and healthy diet",
            "YOU WON'T BELIEVE what happened next!!!",
        ]
        
        labels = [0, 0, 1, 1, 0, 1, 0, 1]  # 0=real, 1=fake
        
        try:
            X = self.vectorizer.fit_transform(sample_news)
            self.model.fit(X, labels)
            self.confidence_model.fit(X, labels)
            self.is_trained = True
            print("Default model initialized")
        except Exception as e:
            print(f"Error initializing default model: {e}")
    
    def predict(self, text):
        """
        Predict if news is fake (1) or real (0)
        """
        if not self.is_trained:
            self.load_model()
        
        try:
            X = self.vectorizer.transform([text])
            prediction = self.model.predict(X)[0]
            return prediction
        except Exception as e:
            print(f"Error in prediction: {e}")
            return 0
    
    def get_confidence(self, text):
        """
        Get confidence score for the prediction
        Returns probability between 0 and 1
        """
        if not self.is_trained:
            self.load_model()
        
        try:
            X = self.vectorizer.transform([text])
            
            # Get probabilities from Naive Bayes
            probabilities = self.model.predict_proba(X)[0]
            
            # Return the higher probability
            confidence = max(probabilities)
            
            return float(confidence)
        except Exception as e:
            print(f"Error getting confidence: {e}")
            return 0.5
    
    def train_model(self, X_train, y_train):
        """Train model with new data"""
        try:
            X_vectorized = self.vectorizer.fit_transform(X_train)
            self.model.fit(X_vectorized, y_train)
            self.confidence_model.fit(X_vectorized, y_train)
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            self.model_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.model_dir / 'classifier.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(self.model_dir / 'vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            print("Model saved successfully")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def get_feature_importance(self, text, top_n=10):
        """Get most important features for prediction"""
        try:
            X = self.vectorizer.transform([text])
            feature_names = np.array(self.vectorizer.get_feature_names_out())
            
            if self.model.coef_.ndim > 1:
                coef = self.model.coef_[0]
            else:
                coef = self.model.coef_
            
            top_indices = np.argsort(np.abs(coef))[-top_n:][::-1]
            top_features = feature_names[top_indices]
            
            return list(top_features)
        except Exception as e:
            print(f"Error getting feature importance: {e}")
            return []
