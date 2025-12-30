import requests
from bs4 import BeautifulSoup
import csv
import json

def install_check():
    """Check if required modules are installed"""
    try:
        import requests
        import bs4
        print("✅ All required modules are installed!")
        return True
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("\nPlease install missing modules:")
        print("pip install requests beautifulsoup4")
        return False

class SimpleWebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_quotes(self):
        """Scrape quotes from quotes.toscrape.com"""
        url = "http://quotes.toscrape.com"
        
        try:
            print(f"Fetching data from {url}...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Check if request was successful
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            quotes = []
            
            # Find all quote containers
            quote_divs = soup.find_all('div', class_='quote')
            
            for quote_div in quote_divs:
                # Extract quote text
                text_tag = quote_div.find('span', class_='text')
                quote_text = text_tag.text if text_tag else "No quote text found"
                
                # Extract author
                author_tag = quote_div.find('small', class_='author')
                author = author_tag.text if author_tag else "Unknown"
                
                # Extract tags
                tags = []
                tags_div = quote_div.find('div', class_='tags')
                if tags_div:
                    tag_links = tags_div.find_all('a', class_='tag')
                    tags = [tag.text for tag in tag_links]
                
                quotes.append({
                    'quote': quote_text,
                    'author': author,
                    'tags': ', '.join(tags)
                })
                
                print(f"✓ Scraped: {quote_text[:50]}... by {author}")
            
            return quotes
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching website: {e}")
            return []
    
    def save_to_file(self, data, filename="quotes.csv", format="csv"):
        """Save data to file"""
        if not data:
            print("No data to save!")
            return
        
        if format.lower() == "csv":
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"✅ Data saved to {filename} (CSV format)")
        
        elif format.lower() == "json":
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to {filename} (JSON format)")
    
    def display_quotes(self, quotes, limit=5):
        """Display quotes in console"""
        print("\n" + "="*60)
        print(f"DISPLAYING FIRST {min(limit, len(quotes))} QUOTES")
        print("="*60)
        
        for i, quote in enumerate(quotes[:limit], 1):
            print(f"\nQuote #{i}:")
            print(f"Quote: {quote['quote']}")
            print(f"Author: {quote['author']}")
            print(f"Tags: {quote['tags']}")
            print("-"*40)

def main():
    """Main function"""
    
    print("="*60)
    print("SIMPLE WEB SCRAPER")
    print("="*60)
    
    # Check if modules are installed
    if not install_check():
        return
    
    # Create scraper instance
    scraper = SimpleWebScraper()
    
    # Scrape quotes
    quotes = scraper.scrape_quotes()
    
    if quotes:
        print(f"\n✅ Successfully scraped {len(quotes)} quotes!")
        
        # Display some quotes
        scraper.display_quotes(quotes, limit=3)
        
        # Save to files
        scraper.save_to_file(quotes, "quotes.csv", "csv")
        scraper.save_to_file(quotes, "quotes.json", "json")
        
        print("\n" + "="*60)
        print("SCRAPING COMPLETED SUCCESSFULLY!")
        print("="*60)
    else:
        print("\n❌ No quotes were scraped. Check your connection or the website.")

# Alternative: Even simpler version if you just want to test
def test_scraper():
    """Test if requests module is working"""
    print("Testing requests module...")
    
    try:
        # Try to import requests
        import requests
        
        # Try a simple GET request
        response = requests.get("http://httpbin.org/status/200", timeout=5)
        
        if response.status_code == 200:
            print("✅ requests module is working correctly!")
            return True
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except ImportError:
        print("❌ requests module is not installed!")
        print("\nTo install, run: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Run test first
    if test_scraper():
        # Then run main scraper
        main()
    else:
        print("\nPlease install the required modules first:")
        print("1. Open terminal/command prompt")
        print("2. Run: pip install requests beautifulsoup4")
        print("3. Run this script again")