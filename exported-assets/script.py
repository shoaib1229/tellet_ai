import requests
from bs4 import BeautifulSoup

# Set a user agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fetch the website content
try:
    url = 'https://tellet.ai/'
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the source code
        source_code = response.text
        
        # Print the first 1000 characters as a preview
        print("Source code preview (first 1000 characters):")
        print(source_code[:1000])
        
        # Print the length of the source code
        print(f"\nTotal source code length: {len(source_code)} characters")
        
        # Use BeautifulSoup to identify main HTML elements
        soup = BeautifulSoup(source_code, 'html.parser')
        
        # Count main HTML elements
        html_elements = {
            'html': len(soup.find_all('html')),
            'head': len(soup.find_all('head')),
            'body': len(soup.find_all('body')),
            'div': len(soup.find_all('div')),
            'script': len(soup.find_all('script')),
            'style': len(soup.find_all('style')),
            'link': len(soup.find_all('link')),
            'a': len(soup.find_all('a')),
            'img': len(soup.find_all('img')),
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
            'p': len(soup.find_all('p'))
        }
        
        print("\nHTML elements count:")
        for element, count in html_elements.items():
            print(f"{element}: {count}")
        
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")