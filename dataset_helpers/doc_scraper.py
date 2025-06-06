import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

class ManimDocScraper:
    def __init__(self):
        self.base_url = "https://docs.manim.community/en/stable/"
        self.examples = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_page(self, url):
        """Scrape a single page and extract code examples and documentation."""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract code blocks
            code_blocks = soup.find_all(['div', 'pre'], class_=['highlight-python', 'highlight-python3', 'python'])
            for block in code_blocks:
                code = block.find('pre').text.strip() if block.name == 'div' else block.text.strip()
                # Get the section title or context
                section = block.find_previous(['h1', 'h2', 'h3'])
                section_title = section.text.strip() if section else "Unknown Section"
                
                # Get the description if available
                description = ""
                prev_elem = block.find_previous(['p', 'div'])
                if prev_elem and prev_elem.name == 'p':
                    description = prev_elem.text.strip()
                
                self.examples.append({
                    'section': section_title,
                    'description': description,
                    'code': code,
                    'source_url': url
                })
            
            # Find links to other pages
            links = soup.find_all('a', href=True)
            return [urljoin(url, link['href']) for link in links 
                   if link['href'].startswith('/') and 
                   not link['href'].startswith('//') and
                   not link['href'].startswith('/_') and
                   not link['href'].endswith('.pdf')]
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []
    
    def scrape_documentation(self):
        """Scrape the entire documentation site."""
        visited = set()
        to_visit = [self.base_url]
        
        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue
                
            visited.add(url)
            
            # Get new links from the page
            new_links = self.scrape_page(url)
            to_visit.extend([link for link in new_links if link not in visited])
            
            # Be nice to the server
            time.sleep(1)
    
    def save_examples(self, filename='manim_doc_examples.json'):
        """Save the scraped examples to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.examples, f, indent=2)
        print(f"Saved {len(self.examples)} examples to {filename}")

if __name__ == "__main__":
    scraper = ManimDocScraper()
    scraper.scrape_documentation()
    scraper.save_examples() 