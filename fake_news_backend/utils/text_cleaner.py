"""
Text Cleaner - Text preprocessing and cleaning
"""

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class TextCleaner:
    """Clean and preprocess text data"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.punctuation = string.punctuation
    
    def clean_text(self, text):
        """
        Clean text by:
        - Lowercasing
        - Removing URLs
        - Removing special characters
        - Removing extra whitespace
        - Removing punctuation
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove html tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, text):
        """Remove common stopwords"""
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)
    
    def remove_punctuation(self, text):
        """Remove punctuation from text"""
        return text.translate(str.maketrans('', '', self.punctuation))
    
    def normalize_whitespace(self, text):
        """Normalize whitespace"""
        return re.sub(r'\s+', ' ', text).strip()
    
    def remove_numbers(self, text):
        """Remove all numbers from text"""
        return re.sub(r'\d+', '', text)
    
    def expand_contractions(self, text):
        """Expand common contractions"""
        contractions_dict = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "could've": "could have",
            "couldn't": "could not",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'll": "he will",
            "he's": "he is",
            "how'd": "how did",
            "how'll": "how will",
            "how's": "how is",
            "i'd": "i would",
            "i'll": "i will",
            "i'm": "i am",
            "i've": "i have",
            "isn't": "is not",
            "it'd": "it would",
            "it'll": "it will",
            "it's": "it is",
            "let's": "let us",
            "shouldn't": "should not",
            "that's": "that is",
            "there's": "there is",
            "they'd": "they would",
            "they'll": "they will",
            "they're": "they are",
            "they've": "they have",
            "wasn't": "was not",
            "we'd": "we would",
            "we'll": "we will",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what's": "what is",
            "won't": "will not",
            "wouldn't": "would not",
            "you'd": "you would",
            "you'll": "you will",
            "you're": "you are",
            "you've": "you have"
        }
        
        for contraction, expansion in contractions_dict.items():
            text = re.sub(r'\b' + contraction + r'\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def preprocess_pipeline(self, text):
        """Complete preprocessing pipeline"""
        # Expand contractions
        text = self.expand_contractions(text)
        
        # Clean text
        text = self.clean_text(text)
        
        # Remove stopwords
        text = self.remove_stopwords(text)
        
        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        return text
