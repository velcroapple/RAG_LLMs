import requests
from bs4 import BeautifulSoup as bs


def get_all_articles():
    wiki_url = f"{BASE_URL}/wiki/Dune_Wiki"
    
    # Store all discovered article URLs
    all_articles = set()
    visited_urls = set()
    urls_to_visit = [wiki_url]
    
    #to show that script is browser-based
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Define which URLs to follow (only wiki articles)
    article_pattern = re.compile(r"^/wiki/(?!Special:|File:|User_blog:|Template:|Category:|Help:|Talk:|User:|MediaWiki:)[^?#]+$")

    count=0
    
    while urls_to_visit:
        current_url = urls_to_visit.pop(0)
        
        if current_url in visited_urls:
            continue
            
        visited_urls.add(current_url)
     
        count+=1
        try:
            print(f"Visiting page {count}: {current_url}")
            response = requests.get(current_url, headers=headers)
            
            if response.status_code == 200:
			#no error!
                soup = bs(response.text, 'html.parser')
                
                # Find all links on the page
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # Only follow internal wiki links
                    if href.startswith('/wiki/') and article_pattern.match(href):
                        full_url = urljoin(BASE_URL, href)
                        
                        if full_url not in visited_urls and full_url not in urls_to_visit:
                            urls_to_visit.append(full_url)
                            all_articles.add(full_url)
            else:
                print(f"Failed to access {current_url}: Status code {response.status_code}")
                
    
            time.sleep(1)
			#so we don't violate the server's rate at which we can send requests
            
        except Exception as e:
            print(f"Error processing {current_url}: {e}")
    
    print(f"Found {len(all_articles)} articles")
    return all_articles
