"""
Fake News Detection System - Backend
Main Flask application with API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
from datetime import datetime

from models.news_classifier import NewsClassifier
from utils.data_processor import DataProcessor
from utils.text_cleaner import TextCleaner

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize classifier and utilities
classifier = NewsClassifier()
processor = DataProcessor()
cleaner = TextCleaner()

# Load model on startup
classifier.load_model()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Fake News Detection API'
    }), 200


@app.route('/api/detect', methods=['POST'])
def detect_fake_news():
    """
    Main endpoint for fake news detection
    Expects JSON with 'news' field containing the article text
    """
    try:
        data = request.get_json()
        
        if not data or 'news' not in data:
            return jsonify({'error': 'Missing "news" field in request'}), 400
        
        news_text = data.get('news', '').strip()
        title = data.get('title', '')
        author = data.get('author', '')
        
        if not news_text:
            return jsonify({'error': 'News text cannot be empty'}), 400
        
        # Clean and process text
        cleaned_text = cleaner.clean_text(news_text)
        
        # Get prediction
        prediction = classifier.predict(cleaned_text)
        
        # Calculate confidence
        confidence = classifier.get_confidence(cleaned_text)
        
        response = {
            'original_text': news_text[:500],  # First 500 chars
            'title': title,
            'author': author,
            'is_fake': prediction == 1,
            'confidence': round(confidence, 4),
            'prediction_label': 'FAKE NEWS' if prediction == 1 else 'REAL NEWS',
            'timestamp': datetime.now().isoformat(),
            'model_version': 'v1.0'
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch-detect', methods=['POST'])
def batch_detect():
    """
    Batch detection for multiple news articles
    Expects JSON with 'articles' array
    """
    try:
        data = request.get_json()
        
        if not data or 'articles' not in data:
            return jsonify({'error': 'Missing "articles" field in request'}), 400
        
        articles = data.get('articles', [])
        
        if not isinstance(articles, list) or len(articles) == 0:
            return jsonify({'error': 'Articles must be a non-empty array'}), 400
        
        if len(articles) > 100:
            return jsonify({'error': 'Maximum 100 articles per request'}), 400
        
        results = []
        
        for article in articles:
            if 'news' not in article:
                continue
            
            news_text = article.get('news', '').strip()
            cleaned_text = cleaner.clean_text(news_text)
            
            prediction = classifier.predict(cleaned_text)
            confidence = classifier.get_confidence(cleaned_text)
            
            results.append({
                'title': article.get('title', ''),
                'is_fake': prediction == 1,
                'confidence': round(confidence, 4),
                'prediction_label': 'FAKE NEWS' if prediction == 1 else 'REAL NEWS'
            })
        
        return jsonify({
            'total_articles': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_detailed():
    """
    Detailed analysis with additional metrics
    """
    try:
        data = request.get_json()
        
        if not data or 'news' not in data:
            return jsonify({'error': 'Missing "news" field'}), 400
        
        news_text = data.get('news', '').strip()
        
        if not news_text:
            return jsonify({'error': 'News text cannot be empty'}), 400
        
        # Clean text
        cleaned_text = cleaner.clean_text(news_text)
        
        # Get detailed analysis
        analysis = processor.analyze_text(news_text, cleaned_text)
        
        # Get prediction
        prediction = classifier.predict(cleaned_text)
        confidence = classifier.get_confidence(cleaned_text)
        
        response = {
            'prediction': 'FAKE NEWS' if prediction == 1 else 'REAL NEWS',
            'confidence': round(confidence, 4),
            'text_stats': {
                'original_length': len(news_text),
                'cleaned_length': len(cleaned_text),
                'word_count': analysis['word_count'],
                'unique_words': analysis['unique_words'],
                'avg_word_length': round(analysis['avg_word_length'], 2),
                'sentence_count': analysis['sentence_count']
            },
            'linguistic_features': {
                'uppercase_ratio': round(analysis['uppercase_ratio'], 4),
                'punctuation_ratio': round(analysis['punctuation_ratio'], 4),
                'exclamation_marks': analysis['exclamation_marks'],
                'question_marks': analysis['question_marks']
            },
            'recommendations': get_recommendations(confidence),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get model statistics and information"""
    return jsonify({
        'model_info': {
            'name': 'Fake News Detection Classifier',
            'version': 'v1.0',
            'model_type': 'TF-IDF + Naive Bayes',
            'accuracy': '0.92',
            'precision': '0.90',
            'recall': '0.94'
        },
        'endpoints': {
            '/api/detect': 'Single article detection',
            '/api/batch-detect': 'Batch detection (up to 100)',
            '/api/analyze': 'Detailed analysis with metrics',
            '/api/stats': 'Model statistics'
        }
    }), 200


def get_recommendations(confidence):
    """Get recommendations based on confidence score"""
    recommendations = []
    
    if confidence < 0.5:
        recommendations.append('Cannot determine with confidence - seek additional sources')
    elif confidence < 0.6:
        recommendations.append('Low confidence - verify with multiple sources')
    elif confidence < 0.7:
        recommendations.append('Moderate confidence - recommended to check sources')
    else:
        recommendations.append('High confidence - verify through fact-checking sites')
    
    recommendations.append('Check author credibility and source')
    recommendations.append('Look for supporting evidence')
    recommendations.append('Compare with other news outlets')
    
    return recommendations


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV', 'production') == 'development'
    )
