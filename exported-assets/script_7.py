import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

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
        
        print("JAVASCRIPT FUNCTIONALITY DOCUMENTATION")
        print("=====================================")
        
        # 1. Detailed script tag analysis
        script_tags = soup.find_all('script')
        
        # Categorize scripts
        print("\n1. SCRIPT TAGS ANALYSIS:")
        
        script_data = []
        for i, script in enumerate(script_tags):
            script_type = script.get('type', 'No type (standard JS)')
            script_src = script.get('src', None)
            script_id = script.get('id', 'No ID')
            script_async = 'async' in script.attrs
            script_defer = 'defer' in script.attrs
            
            # Determine the purpose of the script (estimate)
            purpose = 'Unknown'
            if script_src:
                src_lower = script_src.lower()
                if any(term in src_lower for term in ['gtm', 'ga', 'google-analytics', 'googletagmanager']):
                    purpose = 'Analytics (Google)'
                elif any(term in src_lower for term in ['hotjar', 'clarity', 'heap']):
                    purpose = 'User Behavior Tracking'
                elif any(term in src_lower for term in ['jquery', 'react', 'vue', 'angular']):
                    purpose = 'JavaScript Framework/Library'
                elif any(term in src_lower for term in ['framer']):
                    purpose = 'Framer Framework'
                elif any(term in src_lower for term in ['hubspot', 'marketo', 'salesforce']):
                    purpose = 'Marketing/CRM Integration'
            elif script.string:
                script_content = script.string.lower()
                if any(term in script_content for term in ['gtm', 'ga', 'google-analytics', 'googletagmanager']):
                    purpose = 'Analytics (Google)'
                elif any(term in script_content for term in ['hotjar', 'clarity', 'heap']):
                    purpose = 'User Behavior Tracking'
                elif any(term in script_content for term in ['document.addEventListener', 'window.addEventListener']):
                    purpose = 'Page Interactivity'
                elif any(term in script_content for term in ['framer']):
                    purpose = 'Framer Framework'
                elif any(term in script_content for term in ['form', 'submit', 'validation']):
                    purpose = 'Form Handling'
                
            # Get content preview if inline script
            content_preview = None
            content_length = 0
            if script.string:
                content = script.string.strip()
                content_length = len(content)
                if content:
                    content_preview = (content[:150] + '...') if len(content) > 150 else content
            
            script_data.append({
                'Script #': i+1,
                'Type': script_type,
                'External': bool(script_src),
                'Source URL': script_src,
                'ID': script_id,
                'Async': script_async,
                'Defer': script_defer,
                'Estimated Purpose': purpose,
                'Content Length': content_length,
                'Content Preview': content_preview
            })
            
        # Create a DataFrame
        df_scripts = pd.DataFrame(script_data)
        print(df_scripts[['Script #', 'Type', 'External', 'Source URL', 'Estimated Purpose', 'Content Length']])
        
        # Print content previews separately
        print("\nINLINE SCRIPT CONTENT PREVIEWS:")
        for i, row in df_scripts[df_scripts['Content Preview'].notnull()].iterrows():
            print(f"\nScript #{row['Script #']} - {row['Estimated Purpose']} ({row['Content Length']} chars):")
            print(f"{row['Content Preview']}")
        
        # 2. Event listeners analysis
        print("\n2. EVENT LISTENERS ANALYSIS:")
        
        # Find potential event listeners in inline scripts
        event_patterns = {
            'addEventListener': r'addEventListener\([\'"](\w+)[\'"]',
            'onclick': r'onclick=[\'"]([^"\']+)[\'"]',
            'onload': r'onload=[\'"]([^"\']+)[\'"]',
            'onsubmit': r'onsubmit=[\'"]([^"\']+)[\'"]',
            'jQuery events': r'\$\([^\)]+\)\.on\([\'"](\w+)[\'"]',
            'React events': r'on(\w+)=\{',
        }
        
        event_findings = {}
        
        # Check in all scripts
        all_js_content = ' '.join([script.string for script in script_tags if script.string])
        
        for event_type, pattern in event_patterns.items():
            matches = re.findall(pattern, all_js_content)
            if matches:
                event_findings[event_type] = matches
        
        # Also check in HTML for inline event handlers
        html_content = str(soup)
        for event_type, pattern in event_patterns.items():
            if event_type not in event_findings:
                matches = re.findall(pattern, html_content)
                if matches:
                    event_findings[event_type] = matches
            else:
                # Add any new matches not already found
                new_matches = re.findall(pattern, html_content)
                event_findings[event_type] = list(set(event_findings[event_type] + new_matches))
        
        if event_findings:
            print("Found the following event listeners:")
            for event_type, events in event_findings.items():
                print(f"- {event_type}: {', '.join(set(events[:10]))}{'...' if len(events) > 10 else ''}")
        else:
            print("No explicit event listeners detected")
        
        # 3. DOM manipulation analysis
        print("\n3. DOM MANIPULATION ANALYSIS:")
        
        dom_patterns = {
            'getElementById': r'getElementById\([\'"]([^\'"]+)[\'"]',
            'querySelector': r'querySelector\([\'"]([^\'"]+)[\'"]',
            'querySelectorAll': r'querySelectorAll\([\'"]([^\'"]+)[\'"]',
            'getElementsByClassName': r'getElementsByClassName\([\'"]([^\'"]+)[\'"]',
            'createElement': r'createElement\([\'"](\w+)[\'"]',
            'appendChild': r'appendChild\(',
            'innerHTML': r'innerHTML\s*=',
            'textContent': r'textContent\s*=',
        }
        
        dom_findings = {}
        
        for manip_type, pattern in dom_patterns.items():
            matches = re.findall(pattern, all_js_content)
            if matches:
                dom_findings[manip_type] = matches
            
            # Also check in HTML for potential inline JS
            if manip_type not in dom_findings:
                matches = re.findall(pattern, html_content)
                if matches:
                    dom_findings[manip_type] = matches
        
        if dom_findings:
            print("Found the following DOM manipulation methods:")
            for manip_type, elements in dom_findings.items():
                if elements:
                    print(f"- {manip_type}: {len(elements)} occurrences")
                    if manip_type in ['getElementById', 'querySelector', 'getElementsByClassName']:
                        unique_selectors = set(elements[:5])
                        print(f"  Sample selectors: {', '.join(unique_selectors)}{'...' if len(elements) > 5 else ''}")
        else:
            print("No explicit DOM manipulation detected")
        
        # 4. AJAX/Fetch/API calls analysis
        print("\n4. API INTERACTIONS ANALYSIS:")
        
        api_patterns = {
            'fetch': r'fetch\([\'"]([^\'"]+)[\'"]',
            'XMLHttpRequest': r'XMLHttpRequest\(\)',
            'axios': r'axios\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]',
            'jQuery AJAX': r'\$\.(ajax|get|post)\([\'"]([^\'"]+)[\'"]',
        }
        
        api_findings = {}
        
        for api_type, pattern in api_patterns.items():
            matches = re.findall(pattern, all_js_content)
            if matches:
                api_findings[api_type] = matches
            
            # Also check in HTML for potential inline JS
            if api_type not in api_findings:
                matches = re.findall(pattern, html_content)
                if matches:
                    api_findings[api_type] = matches
        
        if api_findings:
            print("Found the following API/AJAX interactions:")
            for api_type, endpoints in api_findings.items():
                print(f"- {api_type}: {len(endpoints)} occurrences")
                if endpoints:
                    sample = endpoints[:3]
                    print(f"  Sample endpoints: {sample}")
        else:
            print("No explicit API interactions detected")
        
        # 5. Create a summary of JavaScript functionality
        print("\n5. JAVASCRIPT FUNCTIONALITY SUMMARY:")
        
        # Count by purpose
        purpose_counts = df_scripts['Estimated Purpose'].value_counts()
        print("Script purposes:")
        for purpose, count in purpose_counts.items():
            print(f"- {purpose}: {count} script(s)")
        
        # External vs inline
        ext_count = df_scripts['External'].sum()
        inline_count = len(df_scripts) - ext_count
        print(f"\nScript types: {ext_count} external, {inline_count} inline")
        
        # Export to CSV
        df_scripts.to_csv('tellet_ai_javascript_analysis.csv', index=False)
        print("\nJavaScript analysis exported to tellet_ai_javascript_analysis.csv")
            
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")