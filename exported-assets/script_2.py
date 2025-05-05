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
        
        # 1. Extract all script tags
        print("1. JAVASCRIPT COMPONENTS:")
        script_tags = soup.find_all('script')
        print(f"Found {len(script_tags)} script tags")
        
        # Categorize scripts by type
        inline_scripts = []
        external_scripts = []
        
        for script in script_tags:
            src = script.get('src')
            if src:
                external_scripts.append(src)
            elif script.string and len(script.string.strip()) > 0:
                inline_scripts.append(script.string.strip())
        
        print(f"\nExternal JavaScript files: {len(external_scripts)}")
        if external_scripts:
            print("\nSample of external JavaScript URLs:")
            for i, src in enumerate(external_scripts[:5]):  # Show first 5
                print(f"  {i+1}. {src}")
            if len(external_scripts) > 5:
                print(f"  ... and {len(external_scripts)-5} more")
        
        print(f"\nInline JavaScript code blocks: {len(inline_scripts)}")
        if inline_scripts:
            print("\nSample of inline JavaScript (first 300 characters of each):")
            for i, code in enumerate(inline_scripts[:3]):  # Show first 3
                preview = code[:300].replace('\n', ' ').strip()
                print(f"  {i+1}. {preview}...")
            if len(inline_scripts) > 3:
                print(f"  ... and {len(inline_scripts)-3} more code blocks")
        
        # 2. Look for JavaScript frameworks and libraries
        js_frameworks = {
            'react': r'react(-dom)?\.js',
            'vue': r'vue\.js',
            'angular': r'angular(\.min)?\.js',
            'jquery': r'jquery(-\d+\.\d+\.\d+)?(\.min)?\.js',
            'framer': r'framer',
            'gsap': r'gsap',
            'three.js': r'three\.js',
            'tensorflow': r'tensorflow',
            'babylon': r'babylon',
            'stripe': r'stripe',
            'firebase': r'firebase',
            'google analytics': r'ga|gtag|googletagmanager',
            'hotjar': r'hotjar'
        }
        
        print("\n2. JAVASCRIPT FRAMEWORKS/LIBRARIES DETECTION:")
        detected_js_frameworks = []
        
        # Check in script src attributes
        for script in script_tags:
            src = script.get('src', '')
            for name, pattern in js_frameworks.items():
                if re.search(pattern, src, re.IGNORECASE):
                    detected_js_frameworks.append(f"{name} (via script src)")
        
        # Check in the entire HTML for references
        for name, pattern in js_frameworks.items():
            if name not in [fw.split()[0] for fw in detected_js_frameworks]:  # Don't check again if already found
                if re.search(pattern, source_code, re.IGNORECASE):
                    detected_js_frameworks.append(f"{name} (referenced in page)")
        
        if detected_js_frameworks:
            print("Detected JavaScript frameworks/libraries:")
            for framework in detected_js_frameworks:
                print(f"  - {framework}")
        else:
            print("No common JavaScript frameworks detected")
        
        # 3. Identify event listeners and dynamic functionality
        print("\n3. EVENT LISTENERS AND DYNAMIC FUNCTIONALITY:")
        event_patterns = [
            r'addEventListener\([\'"](\w+)[\'"]',
            r'on(\w+)=[\'"]',
            r'\.on\([\'"](\w+)[\'"]'
        ]
        
        all_events = []
        for pattern in event_patterns:
            events = re.findall(pattern, source_code)
            all_events.extend(events)
        
        unique_events = set(all_events)
        if unique_events:
            print(f"Found {len(unique_events)} unique event types:")
            for event in sorted(unique_events):
                print(f"  - {event}")
        else:
            print("No JavaScript event listeners detected in the code")
        
        # 4. Check for Ajax or fetch API usage
        print("\n4. AJAX/FETCH API USAGE:")
        ajax_patterns = [
            r'\.ajax\(',
            r'fetch\(',
            r'XMLHttpRequest',
            r'axios\.'
        ]
        
        ajax_found = False
        for pattern in ajax_patterns:
            if re.search(pattern, source_code):
                ajax_found = True
                print(f"  - Found usage of {pattern.replace('\\', '').replace('(', '').replace('.', '').strip()}")
        
        if not ajax_found:
            print("No AJAX or fetch API usage detected")
            
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")