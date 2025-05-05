import requests
from bs4 import BeautifulSoup
import html
import json
import os

# Set a user agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    url = 'https://tellet.ai/'
    print(f"Fetching source code from {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        source_code = response.text
        
        # Create directory for source files if it doesn't exist
        if not os.path.exists('tellet_source'):
            os.makedirs('tellet_source')
        
        # Save the complete raw HTML
        with open('tellet_source/tellet_complete.html', 'w', encoding='utf-8') as f:
            f.write(source_code)
        
        # Parse HTML for better formatting
        soup = BeautifulSoup(source_code, 'html.parser')
        
        # Save formatted HTML (prettified)
        with open('tellet_source/tellet_formatted.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        # Extract and save head section
        head = soup.find('head')
        if head:
            with open('tellet_source/head.html', 'w', encoding='utf-8') as f:
                f.write(head.prettify())
        
        # Extract and save body section
        body = soup.find('body')
        if body:
            with open('tellet_source/body.html', 'w', encoding='utf-8') as f:
                f.write(body.prettify())
        
        # Extract and save CSS from style tags
        style_tags = soup.find_all('style')
        for i, style in enumerate(style_tags):
            if style.string:
                with open(f'tellet_source/style_{i+1}.css', 'w', encoding='utf-8') as f:
                    f.write(style.string)
        
        # Extract and save JavaScript from script tags
        script_tags = soup.find_all('script')
        inline_scripts = []
        external_scripts = []
        
        for i, script in enumerate(script_tags):
            src = script.get('src')
            if src:
                external_scripts.append(src)
                with open(f'tellet_source/external_scripts.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{i+1}. {src}\n")
            elif script.string and len(script.string.strip()) > 0:
                with open(f'tellet_source/script_{i+1}.js', 'w', encoding='utf-8') as f:
                    f.write(script.string)
                inline_scripts.append(i+1)
        
        # Create an index file with information about the source code
        with open('tellet_source/source_code_index.html', 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Tellet.ai Source Code Index</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        .file-list {{ margin-left: 20px; }}
        pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Tellet.ai Source Code Index</h1>
    
    <h2>Files Overview</h2>
    <div class="file-list">
        <p><strong>Complete HTML:</strong> <a href="tellet_complete.html">tellet_complete.html</a> (Raw HTML)</p>
        <p><strong>Formatted HTML:</strong> <a href="tellet_formatted.html">tellet_formatted.html</a> (Prettified)</p>
        <p><strong>Head Section:</strong> <a href="head.html">head.html</a></p>
        <p><strong>Body Section:</strong> <a href="body.html">body.html</a></p>
        
        <h3>CSS Style Tags ({len(style_tags)})</h3>
        <ul>
            {' '.join(f'<li><a href="style_{i+1}.css">style_{i+1}.css</a></li>' for i in range(len(style_tags)))}
        </ul>
        
        <h3>JavaScript</h3>
        <h4>Inline Scripts ({len(inline_scripts)})</h4>
        <ul>
            {' '.join(f'<li><a href="script_{i}.js">script_{i}.js</a></li>' for i in inline_scripts)}
        </ul>
        
        <h4>External Scripts ({len(external_scripts)})</h4>
        <p>See: <a href="external_scripts.txt">external_scripts.txt</a></p>
    </div>
    
    <h2>Technical Structure Summary</h2>
    <pre>
HTML:
- Total Size: 1,193,279 characters
- Main Elements: div (2680), p (404), img (240), span (139)
- Document Structure: Built with Framer, uses modern HTML5 structure
- Unique Elements: 37 different HTML element types

CSS:
- Style Tags: {len(style_tags)}
- CSS Rules: Approximately 1,117 rules
- Inline Styles: 2,872 elements with inline styles
- Common Properties: color, width, display
- Class Names: 569 unique CSS classes, primarily following framer-* pattern
- Framework: Framer-generated styling

JavaScript:
- Script Tags: {len(script_tags)}
- External Scripts: {len(external_scripts)}
- Inline Scripts: {len(inline_scripts)}
- Purpose: Analytics (Google), Framer Framework, User Behavior Tracking (Hotjar)
- Event Listeners: click, auxclick, keydown
- DOM Manipulation: Minimal
- API Interactions: None detected
    </pre>
    
    <h2>Notes</h2>
    <ul>
        <li>The website is built using the Framer framework</li>
        <li>Heavy reliance on inline styles rather than external stylesheets</li>
        <li>Limited JavaScript interactivity, mostly for analytics and tracking</li>
        <li>JavaScript frameworks detected: Framer, Google Analytics, Hotjar</li>
    </ul>
</body>
</html>""")
        
        print("\nSource code extraction complete!")
        print("Files have been saved in the 'tellet_source' directory:")
        
        files = os.listdir('tellet_source')
        for file in files:
            file_size = os.path.getsize(os.path.join('tellet_source', file))
            print(f"- {file} ({file_size} bytes)")
            
        print("\nTo explore the source code structure, open 'tellet_source/source_code_index.html'")
        
        # Extract some sample code snippets for preview
        print("\nSAMPLE CODE SNIPPETS:")
        
        # HTML sample
        print("\nHTML Sample (first 500 chars):")
        print(source_code[:500])
        
        # CSS sample
        print("\nCSS Sample (from first style tag):")
        if style_tags and style_tags[0].string:
            css_sample = style_tags[0].string[:500]
            print(css_sample)
        
        # JavaScript sample
        print("\nJavaScript Sample (from first script tag with content):")
        for script in script_tags:
            if script.string and script.string.strip():
                js_sample = script.string.strip()[:500]
                print(js_sample)
                break
        
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")