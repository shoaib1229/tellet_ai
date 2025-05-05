import requests
from bs4 import BeautifulSoup
import html
import re

# Set a user agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    url = 'https://tellet.ai/'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        source_code = response.text
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(source_code, 'html.parser')
        
        # 1. Extract the basic document structure
        print("1. BASIC HTML DOCUMENT STRUCTURE")
        print("==================================")
        
        # Get doctype
        doctype = soup.contents[0] if soup.contents and isinstance(soup.contents[0], BeautifulSoup.Doctype) else "No doctype found"
        print(f"DOCTYPE: {doctype}")
        
        # Get HTML tag with attributes
        html_tag = soup.find('html')
        html_attrs = html_tag.attrs if html_tag else {}
        print(f"HTML attributes: {html_attrs}")
        
        # Get HEAD section overview
        head = soup.find('head')
        if head:
            print("\nHEAD SECTION OVERVIEW:")
            print(f"- Title: {soup.title.string if soup.title else 'No title found'}")
            
            # Meta tags
            meta_tags = head.find_all('meta')
            print(f"- Meta tags: {len(meta_tags)} found")
            for i, meta in enumerate(meta_tags[:5], 1):  # Show first 5
                print(f"  {i}. {meta}")
            if len(meta_tags) > 5:
                print(f"  ... and {len(meta_tags)-5} more meta tags")
                
            # Link tags
            link_tags = head.find_all('link')
            print(f"- Link tags: {len(link_tags)} found")
            for i, link in enumerate(link_tags[:5], 1):  # Show first 5
                print(f"  {i}. {link}")
            if len(link_tags) > 5:
                print(f"  ... and {len(link_tags)-5} more link tags")
        
        # Get BODY section overview
        body = soup.find('body')
        if body:
            print("\nBODY SECTION OVERVIEW:")
            body_attrs = body.attrs
            print(f"- Body attributes: {body_attrs}")
            
            # First level divs under body
            main_divs = body.find_all(recursive=False)
            print(f"- Main level elements under body: {len(main_divs)}")
            for i, div in enumerate(main_divs[:3], 1):  # Show first 3
                print(f"  {i}. <{div.name}> with classes: {div.get('class', [])}")
            if len(main_divs) > 3:
                print(f"  ... and {len(main_divs)-3} more main elements")
        
        # 2. Analyze main page structure
        print("\n2. MAIN PAGE STRUCTURE ANALYSIS")
        print("==================================")
        
        # Look for common layout elements
        layout_elements = {
            'header': soup.find_all(['header', 'div'], class_=re.compile('header|nav|top', re.I)),
            'navigation': soup.find_all(['nav', 'ul'], class_=re.compile('nav|menu', re.I)),
            'main': soup.find_all(['main', 'div'], class_=re.compile('main|content', re.I)),
            'sections': soup.find_all('section'),
            'footer': soup.find_all(['footer', 'div'], class_=re.compile('footer|bottom', re.I))
        }
        
        for element_type, elements in layout_elements.items():
            print(f"\n{element_type.upper()} elements found: {len(elements)}")
            if elements:
                for i, elem in enumerate(elements[:2], 1):  # Show first 2 of each type
                    print(f"  {i}. <{elem.name}> with classes: {elem.get('class', [])}")
                    # Print first child element to understand structure
                    first_child = elem.find()
                    if first_child:
                        print(f"     First child: <{first_child.name}> with classes: {first_child.get('class', [])}")
                if len(elements) > 2:
                    print(f"  ... and {len(elements)-2} more {element_type} elements")
        
        # 3. Extract main content headings to understand the structure
        print("\n3. CONTENT HEADINGS STRUCTURE")
        print("==================================")
        
        # Find all headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        # Group by level
        heading_levels = {}
        for h in headings:
            level = h.name
            if level not in heading_levels:
                heading_levels[level] = []
            heading_levels[level].append(h)
        
        for level in sorted(heading_levels.keys()):
            items = heading_levels[level]
            print(f"\n{level.upper()} headings found: {len(items)}")
            for i, item in enumerate(items[:5], 1):  # Show first 5 of each level
                # Clean up text - remove extra whitespace
                text = re.sub(r'\s+', ' ', item.get_text().strip())
                if text:
                    print(f"  {i}. {text[:100]}" + ("..." if len(text) > 100 else ""))
            if len(items) > 5:
                print(f"  ... and {len(items)-5} more {level} headings")
        
        # 4. Summary of overall HTML structure
        print("\n4. HTML STRUCTURE SUMMARY")
        print("==================================")
        
        element_count = {}
        for tag in soup.find_all():
            tag_name = tag.name
            if tag_name not in element_count:
                element_count[tag_name] = 0
            element_count[tag_name] += 1
        
        # Sort by most common elements
        sorted_elements = sorted(element_count.items(), key=lambda x: x[1], reverse=True)
        
        print("Most common HTML elements:")
        for tag, count in sorted_elements[:15]:  # Show top 15
            print(f"  - {tag}: {count}")
        
        print("\nTotal unique HTML elements used: ", len(element_count))
        
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")