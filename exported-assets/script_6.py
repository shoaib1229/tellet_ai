import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
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
        
        print("CSS ORGANIZATION AND ANALYSIS")
        print("=============================")
        
        # 1. Categorize all CSS content by type
        print("\n1. CSS CONTENT CATEGORIZATION:")
        
        # Inline style tags
        style_tags = soup.find_all('style')
        
        # Extract and categorize CSS from style tags
        css_data = []
        
        for i, tag in enumerate(style_tags):
            if tag.string:
                # Identify media queries
                media_queries = re.findall(r'@media\s+([^{]+){([^}]+)}', tag.string, re.DOTALL)
                
                # Count CSS rules (approximate)
                rules_count = len(re.findall(r'[^}]*{[^}]*}', tag.string))
                
                # Extract selectors (approximate)
                selectors = re.findall(r'([^{]+){', tag.string)
                selectors_sample = selectors[:5] if selectors else []
                
                # Look for animations or transitions
                animations = re.findall(r'@keyframes\s+([^{]+){', tag.string)
                has_transitions = 'transition' in tag.string
                
                # Check if it looks like a reset CSS
                is_reset = any(reset_term in tag.string.lower() for reset_term in ['reset', 'normalize', '*{margin:0', '*{padding:0'])
                
                # Determine style category (best guess)
                category = 'Unknown'
                if is_reset:
                    category = 'Reset/Normalize'
                elif animations or has_transitions:
                    category = 'Animation/Transition'
                elif media_queries:
                    category = 'Responsive/Media Queries'
                elif 'font-face' in tag.string:
                    category = 'Typography/Fonts'
                else:
                    # Check common content categories
                    content_indicators = {
                        'Layout': ['grid', 'flex', 'display:', 'position:', 'float:', 'width:', 'height:'],
                        'Typography': ['font-', 'text-', 'line-height'],
                        'Colors/Theme': ['color:', 'background', 'border-color'],
                        'Components': ['button', '.btn', 'nav', 'header', 'footer', '.card']
                    }
                    
                    # Count indicators for each category
                    category_scores = {cat: sum(1 for ind in indicators if ind in tag.string) 
                                      for cat, indicators in content_indicators.items()}
                    
                    # Assign category with highest score if any
                    if any(category_scores.values()):
                        category = max(category_scores.items(), key=lambda x: x[1])[0]
                
                css_data.append({
                    'Style Tag #': i+1,
                    'Category': category,
                    'Rules Count': rules_count,
                    'Has Media Queries': bool(media_queries),
                    'Media Query Types': [mq[0].strip() for mq in media_queries][:3] if media_queries else [],
                    'Has Animations': bool(animations),
                    'Has Transitions': has_transitions,
                    'Selector Examples': selectors_sample,
                    'Size (chars)': len(tag.string)
                })
        
        # Create DataFrame for better readability
        if css_data:
            df = pd.DataFrame(css_data)
            print(df)
            
            # Summary stats
            print("\nCSS SUMMARY STATISTICS:")
            print(f"Total style tags: {len(style_tags)}")
            print(f"Total CSS rules (approximate): {df['Rules Count'].sum()}")
            print(f"Total CSS size (chars): {df['Size (chars)'].sum()}")
            
            # Categories distribution
            print("\nCSS CATEGORIES DISTRIBUTION:")
            category_counts = df['Category'].value_counts()
            for category, count in category_counts.items():
                print(f"- {category}: {count} style block(s)")
        else:
            print("No CSS style tags found with content")
            
        # External CSS files
        print("\n2. EXTERNAL CSS FILES:")
        css_links = soup.find_all('link', rel='stylesheet')
        if css_links:
            print(f"Found {len(css_links)} external CSS files:")
            for i, link in enumerate(css_links):
                print(f"  {i+1}. {link.get('href', 'No href attribute')}")
        else:
            print("No external CSS files found")
        
        # Inline styles on elements
        print("\n3. INLINE STYLES ANALYSIS:")
        elements_with_style = soup.find_all(attrs={"style": True})
        print(f"Elements with inline style attributes: {len(elements_with_style)}")
        
        if elements_with_style:
            # Analyze common inline style properties
            all_styles = ' '.join([elem.get('style', '') for elem in elements_with_style])
            
            # Count common properties
            common_properties = [
                'color', 'background', 'margin', 'padding', 'width', 'height', 
                'display', 'position', 'font', 'border', 'transform', 'opacity'
            ]
            
            property_counts = {}
            for prop in common_properties:
                count = len(re.findall(fr'{prop}\s*:', all_styles))
                if count > 0:
                    property_counts[prop] = count
            
            # Sort by most common
            sorted_props = sorted(property_counts.items(), key=lambda x: x[1], reverse=True)
            
            print("\nMost common inline style properties:")
            for prop, count in sorted_props[:10]:
                print(f"- {prop}: {count} occurrences")
            
            # Sample of elements with inline styles
            print("\nSample of elements with inline styles:")
            for i, elem in enumerate(elements_with_style[:5]):
                print(f"  {i+1}. <{elem.name}> with style: {elem.get('style')[:100]}...")
        
        # Export a CSS organization summary to CSV
        if css_data:
            summary_df = df[['Style Tag #', 'Category', 'Rules Count', 'Has Media Queries', 
                             'Has Animations', 'Has Transitions', 'Size (chars)']]
            summary_df.to_csv('tellet_ai_css_summary.csv', index=False)
            print("\nCSS summary exported to tellet_ai_css_summary.csv")
            
        # 4. CSS Class Names Analysis
        print("\n4. CSS CLASS NAMES ANALYSIS:")
        elements_with_classes = soup.find_all(class_=True)
        all_classes = []
        for elem in elements_with_classes:
            all_classes.extend(elem.get('class', []))
        
        class_counts = {}
        for cls in all_classes:
            if cls not in class_counts:
                class_counts[cls] = 0
            class_counts[cls] += 1
        
        # Look for naming patterns
        class_patterns = {}
        for cls in class_counts:
            # Extract prefix (e.g., "framer-" from "framer-1a2b3c")
            match = re.match(r'^([a-zA-Z0-9_-]+)-', cls)
            if match:
                prefix = match.group(1)
                if prefix not in class_patterns:
                    class_patterns[prefix] = 0
                class_patterns[prefix] += 1
        
        # Sort patterns by frequency
        sorted_patterns = sorted(class_patterns.items(), key=lambda x: x[1], reverse=True)
        
        print(f"Total unique class names: {len(class_counts)}")
        print("\nClass name patterns (prefixes):")
        for pattern, count in sorted_patterns[:5]:
            print(f"- {pattern}-*: {count} classes")
        
        print("\nMost common class names:")
        sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)
        for cls, count in sorted_classes[:10]:
            print(f"- {cls}: {count} occurrences")
            
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")