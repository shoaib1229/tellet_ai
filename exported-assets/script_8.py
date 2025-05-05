import pandas as pd

# Create a comprehensive summary of tellet.ai website structure
summary = {
    "Website": "Tellet.ai",
    "Technical Structure": {
        "HTML": {
            "Total Size": "1,193,279 characters",
            "Main Elements": {
                "div": 2680,
                "p": 404,
                "img": 240,
                "span": 139,
                "a": 95,
                "h5": 40,
                "h1": 23,
                "section": 22
            },
            "Document Structure": "Built with Framer, uses modern HTML5 structure",
            "Unique Elements": "37 different HTML element types"
        },
        "CSS": {
            "Style Tags": 2,
            "CSS Rules": "Approximately 1,117 rules",
            "Inline Styles": "2,872 elements with inline styles",
            "Common Properties": ["color", "width", "display"],
            "Class Names": "569 unique CSS classes, primarily following framer-* pattern",
            "Most Common Classes": ["framer-text (520 occurrences)", "framer-XRQDu (105 occurrences)"],
            "Framework": "Framer-generated styling"
        },
        "JavaScript": {
            "Script Tags": 10,
            "External Scripts": 4,
            "Inline Scripts": 6,
            "Purpose": {
                "Analytics (Google)": 3,
                "Framer Framework": 3,
                "User Behavior Tracking (Hotjar)": 1,
                "Unknown": 3
            },
            "Event Listeners": ["click", "auxclick", "keydown"],
            "DOM Manipulation": "Minimal (querySelectorAll, createElement, appendChild)",
            "API Interactions": "None detected"
        }
    },
    "Content Structure": {
        "Main Sections": {
            "Header": "Marketing headline and key features",
            "Value Propositions": "Features multi-column layout explaining key benefits",
            "How It Works": "Step-by-step explanation of the product",
            "Testimonials": "Customer quotes and endorsements",
            "Call to Action": "Contact/demo request"
        },
        "Key Messages": [
            "AI-powered interview tool",
            "Conduct hundreds of interviews at once",
            "Analyze results quickly",
            "Support for 57 languages",
            "Get rich insights with voice/video responses",
            "Ask follow-up questions to transcripts"
        ]
    },
    "Overall Assessment": {
        "Technology": "Built with Framer, modern web technologies",
        "Performance": "Heavy page weight (1.1MB+ of HTML)",
        "SEO": "Uses standard meta tags, clean URL structure",
        "Accessibility": "Uses semantic HTML elements",
        "Responsive Design": "Uses media queries for adaptation to different devices"
    }
}

# Convert to DataFrame for better display
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Create a simplified version for display
display_summary = {
    "Category": [],
    "Key": [],
    "Value": []
}

# HTML summary
display_summary["Category"].append("HTML")
display_summary["Key"].append("Total Size")
display_summary["Value"].append("1,193,279 characters")

display_summary["Category"].append("HTML")
display_summary["Key"].append("Common Elements")
display_summary["Value"].append("div (2680), p (404), img (240), span (139)")

display_summary["Category"].append("HTML")
display_summary["Key"].append("Document Structure")
display_summary["Value"].append("Built with Framer, uses modern HTML5 structure with 37 unique elements")

# CSS summary
display_summary["Category"].append("CSS")
display_summary["Key"].append("Style Tags & Rules")
display_summary["Value"].append("2 style tags with approximately 1,117 CSS rules")

display_summary["Category"].append("CSS")
display_summary["Key"].append("Inline Styles")
display_summary["Value"].append("2,872 elements with inline styles (color, width, display most common)")

display_summary["Category"].append("CSS")
display_summary["Key"].append("Class Structure")
display_summary["Value"].append("569 unique CSS classes, primarily using framer-* naming pattern")

# JavaScript summary
display_summary["Category"].append("JavaScript")
display_summary["Key"].append("Script Tags")
display_summary["Value"].append("10 total (4 external, 6 inline)")

display_summary["Category"].append("JavaScript")
display_summary["Key"].append("Functionality")
display_summary["Value"].append("Analytics, Framer Framework, User Tracking (Hotjar)")

display_summary["Category"].append("JavaScript")
display_summary["Key"].append("Interactivity")
display_summary["Value"].append("Basic event listeners (click, keydown), minimal DOM manipulation")

# Content summary
display_summary["Category"].append("Content")
display_summary["Key"].append("Main Sections")
display_summary["Value"].append("Header, Value Propositions, How It Works, Testimonials, Call to Action")

display_summary["Category"].append("Content")
display_summary["Key"].append("Key Messages")
display_summary["Value"].append("AI interviews, multi-language support, quick analysis, rich voice/video responses")

# Overall assessment
display_summary["Category"].append("Overall")
display_summary["Key"].append("Technology & Performance")
display_summary["Value"].append("Framer-built site with heavy page weight (1.1MB+)")

display_summary["Category"].append("Overall")
display_summary["Key"].append("Design & Accessibility")
display_summary["Value"].append("Modern responsive design using media queries, semantic HTML elements")

# Create and display DataFrame
df = pd.DataFrame(display_summary)
print("COMPREHENSIVE SUMMARY OF TELLET.AI WEBSITE STRUCTURE")
print("===================================================")
print(df.to_string(index=False))

# Export to CSV
df.to_csv("tellet_ai_website_summary.csv", index=False)
print("\nSummary exported to tellet_ai_website_summary.csv")

# Generate a textual summary that's easy to read
print("\nTEXTUAL SUMMARY")
print("===============")
print("Tellet.ai is a marketing website for an AI-powered interview and research tool.")
print("\nTECHNICAL STRUCTURE:")
print("- Built using Framer framework with a large HTML document (1.1MB+)")
print("- Heavy use of div elements (2,680) with minimal semantic structure")
print("- Styling relies on 2 style tags containing 1,117 CSS rules and 2,872 inline styles")
print("- 569 unique CSS classes following Framer's naming pattern (framer-*)")
print("- JavaScript functionality includes 10 script tags for analytics (Google), behavior tracking (Hotjar), and core Framer functionality")
print("- Minimal interactivity with basic event listeners and DOM manipulation")
print("\nCONTENT STRUCTURE:")
print("- Marketing-focused copy highlights AI-powered interview capabilities")
print("- Key features: conducting hundreds of interviews at once, multi-language support (57 languages), voice/video responses")
print("- Includes testimonials from customers like Royal Swinkels, Humanise, Vodafone Ziggo, and Blauw research")
print("- Call-to-action focuses on demo requests")
print("\nOVERALL ASSESSMENT:")
print("- Professional marketing site with modern design techniques")
print("- Heavy page weight may impact performance")
print("- Strong focus on visual presentation rather than technical optimization")
print("- Built for marketing purposes with clear user journey toward demo/contact")