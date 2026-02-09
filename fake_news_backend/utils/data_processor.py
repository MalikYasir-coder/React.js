"""
Data Processor - Text analysis and feature extraction
"""

import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string


class DataProcessor:
    """Process and analyze text data"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_text(self, original_text, cleaned_text):
        """
        Analyze text and extract features
        """
        words = word_tokenize(cleaned_text.lower())
        sentences = sent_tokenize(original_text)
        
        # Basic statistics
        word_count = len(words)
        unique_words = len(set(words))
        avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0
        sentence_count = len(sentences)
        
        # Special characters analysis
        uppercase_count = sum(1 for c in original_text if c.isupper())
        uppercase_ratio = uppercase_count / len(original_text) if len(original_text) > 0 else 0
        
        punctuation_count = sum(1 for c in original_text if c in string.punctuation)
        punctuation_ratio = punctuation_count / len(original_text) if len(original_text) > 0 else 0
        
        exclamation_marks = original_text.count('!')
        question_marks = original_text.count('?')
        
        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'avg_word_length': avg_word_length,
            'sentence_count': sentence_count,
            'uppercase_ratio': uppercase_ratio,
            'punctuation_ratio': punctuation_ratio,
            'exclamation_marks': exclamation_marks,
            'question_marks': question_marks
        }
    
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top N words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [word for word, freq in top_words]
    
    def get_sentiment_indicators(self, text):
        """Get sentiment indicators (basic)"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'dreadful']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'sentiment_ratio': positive_count - negative_count
        }
