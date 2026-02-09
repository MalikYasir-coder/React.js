"""
Example client for using the Fake News Detection API
Can be used for testing or as a reference for frontend integration
"""

import requests
import json
from typing import Dict, List, Optional


class FakeNewsDetectionClient:
    """Client for interacting with the Fake News Detection API"""
    
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check if the API is running"""
        try:
            response = self.session.get(f'{self.base_url}/health')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status': 'unhealthy'}
    
    def detect_fake_news(self, 
                        news_text: str, 
                        title: str = '', 
                        author: str = '') -> Dict:
        """
        Detect if a single news article is fake
        
        Args:
            news_text: The article text
            title: Article title (optional)
            author: Author name (optional)
        
        Returns:
            Dictionary with prediction and confidence
        """
        payload = {
            'news': news_text,
            'title': title,
            'author': author
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/detect',
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def batch_detect(self, articles: List[Dict]) -> Dict:
        """
        Detect fake news for multiple articles
        
        Args:
            articles: List of article dictionaries with 'news' and optional 'title'
        
        Returns:
            Dictionary with batch results
        """
        payload = {'articles': articles}
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/batch-detect',
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def analyze_detailed(self, news_text: str) -> Dict:
        """
        Get detailed analysis of an article
        
        Args:
            news_text: The article text
        
        Returns:
            Dictionary with detailed metrics and analysis
        """
        payload = {'news': news_text}
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/analyze',
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def get_model_stats(self) -> Dict:
        """Get model information and statistics"""
        try:
            response = self.session.get(f'{self.base_url}/api/stats')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}


def print_detection_result(result: Dict):
    """Pretty print detection results"""
    print("\n" + "="*60)
    print("DETECTION RESULT")
    print("="*60)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Prediction: {result.get('prediction_label', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 'N/A'):.2%}")
    print(f"Timestamp: {result.get('timestamp', 'N/A')}")
    
    if 'title' in result and result['title']:
        print(f"Title: {result['title']}")
    
    print("="*60 + "\n")


def print_detailed_analysis(result: Dict):
    """Pretty print detailed analysis"""
    print("\n" + "="*80)
    print("DETAILED ANALYSIS")
    print("="*80)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Prediction: {result.get('prediction', 'N/A')}")
    print(f"Confidence: {result.get('confidence', 'N/A'):.2%}")
    
    print("\nText Statistics:")
    stats = result.get('text_stats', {})
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nLinguistic Features:")
    features = result.get('linguistic_features', {})
    for key, value in features.items():
        print(f"  {key}: {value}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(result.get('recommendations', []), 1):
        print(f"  {i}. {rec}")
    
    print("="*80 + "\n")


if __name__ == '__main__':
    # Initialize client
    client = FakeNewsDetectionClient('http://localhost:5000')
    
    # Check if API is running
    print("Checking API health...")
    health = client.health_check()
    if 'error' in health:
        print(f"Failed to connect: {health['error']}")
        print("Make sure the Flask server is running with: python app.py")
        exit(1)
    
    print("✓ API is healthy\n")
    
    # Example 1: Single detection
    print("Example 1: Single Article Detection")
    print("-" * 60)
    
    test_article_1 = """
    Scientists have discovered a breakthrough treatment that could revolutionize 
    healthcare. The new drug has shown promising results in clinical trials with 
    significant improvements in patient outcomes. Further research is ongoing.
    """
    
    result = client.detect_fake_news(
        news_text=test_article_1,
        title="Breaking: Scientists Discover New Medical Breakthrough",
        author="Dr. Smith"
    )
    print_detection_result(result)
    
    # Example 2: Suspicious article
    print("Example 2: Potentially Suspicious Article")
    print("-" * 60)
    
    test_article_2 = """
    SHOCKING TRUTH REVEALED!!! Celebrities DON'T want you to know this one trick!
    This AMAZING secret will change your life FOREVER!!! Don't miss out!!!
    """
    
    result = client.detect_fake_news(
        news_text=test_article_2,
        title="You Won't Believe What Happened Next!"
    )
    print_detection_result(result)
    
    # Example 3: Detailed analysis
    print("Example 3: Detailed Analysis")
    print("-" * 60)
    
    result = client.analyze_detailed(test_article_1)
    print_detailed_analysis(result)
    
    # Example 4: Batch detection
    print("Example 4: Batch Detection")
    print("-" * 60)
    
    articles = [
        {'news': test_article_1, 'title': 'Article 1'},
        {'news': test_article_2, 'title': 'Article 2'},
    ]
    
    result = client.batch_detect(articles)
    print(f"\nBatch Detection Results:")
    print(f"Total articles processed: {result.get('total_articles', 0)}")
    print(f"Timestamp: {result.get('timestamp', 'N/A')}")
    
    if 'results' in result:
        for i, res in enumerate(result['results'], 1):
            print(f"\n  Article {i}: {res['title']}")
            print(f"    Prediction: {res['prediction_label']}")
            print(f"    Confidence: {res['confidence']:.2%}")
    
    # Example 5: Model stats
    print("\n\nExample 5: Model Statistics")
    print("-" * 60)
    
    stats = client.get_model_stats()
    print(json.dumps(stats, indent=2))
    
    print("\n✓ Examples completed!")
