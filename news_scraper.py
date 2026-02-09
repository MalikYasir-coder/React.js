"""
News Headlines Scraper
This script scrapes news headlines from a website using requests and BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def scrape_bbc_news():
    """Scrape headlines from BBC News"""
    try:
        url = "https://www.bbc.com/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find headline elements (BBC News structure)
        headlines = []
        
        # Target common headline selectors
        for item in soup.find_all(['h2', 'h3'], limit=15):
            text = item.get_text(strip=True)
            link_tag = item.find_parent('a')
            link = link_tag['href'] if link_tag and link_tag.get('href') else "No link"
            
            if text and len(text) > 10:  # Filter out very short text
                headlines.append({
                    'title': text,
                    'link': link if link.startswith('http') else f"https://www.bbc.com{link}"
                })
        
        return headlines[:10]  # Return top 10
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BBC News: {e}")
        return []


def scrape_techcrunch():
    """Scrape headlines from TechCrunch"""
    try:
        url = "https://techcrunch.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        headlines = []
        
        # Find articles (TechCrunch often uses specific article elements)
        for article in soup.find_all('a', class_='post-block__title__link', limit=10):
            text = article.get_text(strip=True)
            link = article.get('href', 'No link')
            
            if text:
                headlines.append({
                    'title': text,
                    'link': link
                })
        
        return headlines
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TechCrunch: {e}")
        return []


def scrape_generic(url, headline_selector='h2'):
    """Generic scraper for any website - customize the selector as needed"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        headlines = []
        
        for element in soup.find_all(headline_selector, limit=10):
            text = element.get_text(strip=True)
            link_tag = element.find_parent('a')
            link = link_tag['href'] if link_tag and link_tag.get('href') else "No link"
            
            if text and len(text) > 5:
                headlines.append({
                    'title': text,
                    'link': link
                })
        
        return headlines
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def save_to_json(headlines, filename='headlines.json'):
    """Save scraped headlines to JSON file"""
    data = {
        'scraped_at': datetime.now().isoformat(),
        'headlines': headlines
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Headlines saved to {filename}")


def display_headlines(headlines, source_name="Headlines"):
    """Display headlines in a formatted way"""
    print(f"\n{'='*80}")
    print(f"{source_name} ({len(headlines)} headlines)")
    print(f"{'='*80}\n")
    
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline['title']}")
        if headline['link'] != "No link":
            print(f"   Link: {headline['link']}\n")
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    print("Starting News Headlines Scraper...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Scrape BBC News
    print("Scraping BBC News...")
    bbc_headlines = scrape_bbc_news()
    if bbc_headlines:
        display_headlines(bbc_headlines, "BBC News")
        save_to_json(bbc_headlines, 'bbc_headlines.json')
    else:
        print("No headlines found from BBC News.\n")
    
    # Scrape TechCrunch
    print("Scraping TechCrunch...")
    tech_headlines = scrape_techcrunch()
    if tech_headlines:
        display_headlines(tech_headlines, "TechCrunch")
        save_to_json(tech_headlines, 'techcrunch_headlines.json')
    else:
        print("No headlines found from TechCrunch.\n")
    
    print("Scraping complete!")
