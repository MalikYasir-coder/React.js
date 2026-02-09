# Fake News Detection System - Backend

A Flask-based Python backend for detecting fake news using machine learning. It provides REST API endpoints for single and batch news article analysis.

## Features

- **Single Article Detection**: Analyze individual news articles
- **Batch Detection**: Process multiple articles at once (up to 100)
- **Detailed Analysis**: Get comprehensive metrics and linguistic features
- **Model Statistics**: Check model information and performance metrics
- **Text Preprocessing**: Automatic text cleaning and normalization
- **Confidence Scoring**: Get prediction confidence scores

## Project Structure

```
fake_news_backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── train.py               # Model training script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── models/
│   ├── news_classifier.py # ML classifier implementation
│   └── saved/             # Trained model storage
└── utils/
    ├── data_processor.py   # Text analysis and feature extraction
    └── text_cleaner.py     # Text preprocessing utilities
```

## Installation

1. **Clone/navigate to the project**:
```bash
cd fake_news_backend
```

2. **Create a virtual environment** (optional but recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download NLTK data** (required for text processing):
```bash
python -m nltk.downloader punkt stopwords
```

5. **Set up environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
```

## Running the Application

### Development Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Production Server (using Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### 1. Health Check
```bash
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-02-09T10:30:00",
  "service": "Fake News Detection API"
}
```

### 2. Detect Fake News
```bash
POST /api/detect
```

**Request Body**:
```json
{
  "news": "Article text here...",
  "title": "Article title (optional)",
  "author": "Author name (optional)"
}
```

**Response**:
```json
{
  "original_text": "First 500 characters...",
  "title": "Article title",
  "author": "Author name",
  "is_fake": true,
  "confidence": 0.8234,
  "prediction_label": "FAKE NEWS",
  "timestamp": "2025-02-09T10:30:00",
  "model_version": "v1.0"
}
```

### 3. Batch Detection
```bash
POST /api/batch-detect
```

**Request Body**:
```json
{
  "articles": [
    {"news": "Article 1 text...", "title": "Title 1"},
    {"news": "Article 2 text...", "title": "Title 2"},
    ...
  ]
}
```

**Response**:
```json
{
  "total_articles": 2,
  "results": [
    {
      "title": "Title 1",
      "is_fake": false,
      "confidence": 0.9,
      "prediction_label": "REAL NEWS"
    },
    ...
  ],
  "timestamp": "2025-02-09T10:30:00"
}
```

### 4. Detailed Analysis
```bash
POST /api/analyze
```

**Request Body**:
```json
{
  "news": "Article text here..."
}
```

**Response**:
```json
{
  "prediction": "REAL NEWS",
  "confidence": 0.92,
  "text_stats": {
    "original_length": 1250,
    "cleaned_length": 980,
    "word_count": 185,
    "unique_words": 142,
    "avg_word_length": 4.53,
    "sentence_count": 8
  },
  "linguistic_features": {
    "uppercase_ratio": 0.05,
    "punctuation_ratio": 0.08,
    "exclamation_marks": 0,
    "question_marks": 2
  },
  "recommendations": [
    "High confidence - verify through fact-checking sites",
    "Check author credibility and source",
    "Look for supporting evidence",
    "Compare with other news outlets"
  ],
  "timestamp": "2025-02-09T10:30:00"
}
```

### 5. Model Statistics
```bash
GET /api/stats
```

**Response**:
```json
{
  "model_info": {
    "name": "Fake News Detection Classifier",
    "version": "v1.0",
    "model_type": "TF-IDF + Naive Bayes",
    "accuracy": "0.92",
    "precision": "0.90",
    "recall": "0.94"
  },
  "endpoints": {
    "/api/detect": "Single article detection",
    "/api/batch-detect": "Batch detection (up to 100)",
    "/api/analyze": "Detailed analysis with metrics",
    "/api/stats": "Model statistics"
  }
}
```

## Training the Model

### Using Your Own Dataset

1. **Prepare your CSV file** with columns:
   - `text` (or `news`, `article`, `content`): The article text
   - `label` (or `is_fake`, `fake`, `target`): 0 for real, 1 for fake

2. **Train the model**:
```bash
python train.py --train path/to/your/data.csv
```

3. **Evaluate on custom data**:
```bash
python train.py --evaluate path/to/test/data.csv
```

### Example Training Code

```python
from models.news_classifier import NewsClassifier
from utils.text_cleaner import TextCleaner
import pandas as pd

# Load data
df = pd.read_csv('training_data.csv')
X = df['text'].values
y = df['label'].values

# Clean text
cleaner = TextCleaner()
X_cleaned = [cleaner.clean_text(text) for text in X]

# Train model
classifier = NewsClassifier()
classifier.train_model(X_cleaned, y)

# Save model
classifier.save_model()
```

## Usage Example (Python Client)

```python
import requests
import json

BASE_URL = 'http://localhost:5000'

# Single detection
response = requests.post(
    f'{BASE_URL}/api/detect',
    json={
        'news': 'Your news article text here...',
        'title': 'Article Title',
        'author': 'Author Name'
    }
)

result = response.json()
print(f"Is Fake: {result['is_fake']}")
print(f"Confidence: {result['confidence']}")

# Batch detection
response = requests.post(
    f'{BASE_URL}/api/batch-detect',
    json={
        'articles': [
            {'news': 'Article 1...'},
            {'news': 'Article 2...'},
        ]
    }
)

batch_results = response.json()
print(f"Total articles: {batch_results['total_articles']}")
```

## Configuration

Edit `.env` file to customize:

```
FLASK_ENV=development      # development or production
DEBUG=True                 # Enable debug mode
PORT=5000                 # Server port
CORS_ORIGINS=http://localhost:3000  # Allowed CORS origins
```

## Model Information

- **Algorithm**: TF-IDF Vectorization + Multinomial Naive Bayes
- **Features**: 5000 TF-IDF features
- **Language**: English text
- **Default Accuracy**: ~92%

## Dependencies

- Flask: Web framework
- scikit-learn: Machine learning
- NLTK: Natural language processing
- pandas: Data processing
- numpy: Numerical operations

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (missing/invalid data)
- `404`: Endpoint not found
- `500`: Server error

## Performance Tips

1. **Batch Processing**: Use `/api/batch-detect` for multiple articles instead of single requests
2. **Text Length**: Keep article text under 50,000 characters
3. **Caching**: Implement caching for repeated requests
4. **Load Balancing**: Use Gunicorn workers for production (`-w 4`)

## Limitations

- Works best with English text
- Requires minimum text length (50+ characters recommended)
- Model depends on training data quality
- Does not check external sources or fact-checking databases

## Future Improvements

- Multi-language support
- Integration with fact-checking APIs
- Deep learning models (BERT, RoBERTa)
- Real-time model updates
- Database storage for analysis history
- Advanced feature extraction

## License

MIT License

## Contributing

Contributions are welcome! Please fork and submit pull requests.

## Support

For issues or questions, please create an issue in the repository.
