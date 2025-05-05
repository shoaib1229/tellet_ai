import requests
from bs4 import BeautifulSoup
import re
import json

# Set a user agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    url = 'https://tellet.ai/'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        source_code = response.text
        soup = BeautifulSoup(source_code, 'html.parser')
        
        # 1. Extract inline CSS styles
        print("1. INLINE CSS STYLES:")
        style_tags = soup.find_all('style')
        print(f"Found {len(style_tags)} style tags")
        
        if style_tags:
            # Print the first style tag content (truncated if too long)
            first_style = style_tags[0].string
            if first_style:
                preview_length = min(500, len(first_style))
                print(f"\nPreview of first style tag ({preview_length} characters):")
                print(first_style[:preview_length])
                print("..." if len(first_style) > preview_length else "")
            else:
                print("First style tag is empty or None")
        
        # 2. Extract external CSS links
        print("\n2. EXTERNAL CSS LINKS:")
        css_links = soup.find_all('link', rel='stylesheet')
        print(f"Found {len(css_links)} external CSS stylesheet links")
        
        if css_links:
            print("\nExternal CSS URLs:")
            for i, link in enumerate(css_links[:5]):  # Show first 5 links
                print(f"  {i+1}. {link.get('href', 'No href attribute')}")
            if len(css_links) > 5:
                print(f"  ... and {len(css_links)-5} more")
        
        # 3. Find inline style attributes
        elements_with_style = soup.find_all(attrs={"style": True})
        print(f"\nFound {len(elements_with_style)} HTML elements with inline style attributes")
        
        if elements_with_style:
            print("\nSample of elements with inline styles:")
            for i, element in enumerate(elements_with_style[:3]):  # Show first 3 elements
                tag_name = element.name
                style_attr = element.get('style')
                print(f"  {i+1}. <{tag_name}> element with style: {style_attr}")
            if len(elements_with_style) > 3:
                print(f"  ... and {len(elements_with_style)-3} more")
        
        # 4. Extract CSS classes used
        all_elements = soup.find_all(class_=True)
        all_classes = []
        for element in all_elements:
            all_classes.extend(element.get('class', []))
        
        unique_classes = set(all_classes)
        print(f"\nFound {len(unique_classes)} unique CSS class names")
        
        if unique_classes:
            print("\nSample of CSS class names:")
            sample_classes = list(unique_classes)[:10]  # Show first 10 classes
            for i, class_name in enumerate(sample_classes):
                print(f"  {i+1}. {class_name}")
            if len(unique_classes) > 10:
                print(f"  ... and {len(unique_classes)-10} more")
        
        # 5. Look for any CSS frameworks or library references
        frameworks = {
            'bootstrap': r'bootstrap.*\.css',
            'tailwind': r'tailwind.*\.css',
            'material': r'material.*\.css',
            'foundation': r'foundation.*\.css',
            'bulma': r'bulma.*\.css',
            'semantic-ui': r'semantic.*\.css',
            'framer': r'framer'
        }
        
        print("\n5. CSS FRAMEWORKS DETECTION:")
        detected_frameworks = []
        
        for name, pattern in frameworks.items():
            # Check in link hrefs
            for link in soup.find_all('link'):
                href = link.get('href', '')
                if re.search(pattern, href, re.IGNORECASE):
                    detected_frameworks.append(f"{name} (via link tag)")
                    break
            
            # Check in the entire HTML
            if name not in [fw.split()[0] for fw in detected_frameworks]:  # Don't check again if already found
                if re.search(pattern, source_code, re.IGNORECASE):
                    detected_frameworks.append(f"{name} (referenced in page)")
        
        if detected_frameworks:
            print("Detected CSS frameworks/libraries:")
            for framework in detected_frameworks:
                print(f"  - {framework}")
        else:
            print("No common CSS frameworks detected")
            
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")