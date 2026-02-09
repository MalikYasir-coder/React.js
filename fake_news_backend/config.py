"""
Configuration for Fake News Detection Backend
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Environment variables
DEBUG = os.getenv('DEBUG', 'False') == 'True'
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
PORT = int(os.getenv('PORT', 5000))

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///fake_news.db')

# ML Model configuration
MODEL_PATH = BASE_DIR / 'models' / 'saved' / 'classifier.pkl'
VECTORIZER_PATH = BASE_DIR / 'models' / 'saved' / 'vectorizer.pkl'

# API configuration
MAX_ARTICLES_BATCH = 100
MAX_TEXT_LENGTH = 50000

# CORS configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
