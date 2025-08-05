from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
app.config['APP_NAME'] = 'WebSage'

# Load environment variables from a .env file
# Note: For Vercel deployments, you should set these as environment variables in the project settings.
load_dotenv()

# Configure Gemini AI
google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    # This check is good practice, but on Vercel, the build would fail before this
    # if the environment variable wasn't set.
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash') 

def scrapeweb(url):
    """
    Scrapes the given URL and returns the prettified HTML content.
    Uses requests and BeautifulSoup, which are lightweight libraries.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        # This truncates the content to a reasonable size to avoid API limits and reduce
        # processing time. You might need to adjust this depending on the average page size.
        return soup.prettify()[:25000] # Truncate to 25KB

    except requests.RequestException as e:
        return f"Error scraping {url}: {str(e)}"
    
@app.route('/')
def home():
    """
    Renders the main page of the application.
    """
    return render_template('index.html')

@app.route('/scrape', methods=['POST']) 
def scrape():
    """
    Receives a URL and a query, scrapes the page, and uses the Gemini API
    to answer the query based on the page content.
    """
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        url = data.get('url')
        query = data.get('query')

        if not url or not query:
            return jsonify({
                'success': False,
                'error': 'URL and query are required'
            }), 400

        content = scrapeweb(url)
        if content.startswith('Error scraping'):
            return jsonify({
                'success': False,
                'error': content
            }), 400
        
        # The prompt is constructed to give the AI context and instructions.
        prompt = f"""
You are an expert web content analyst.

Analyze the following HTML content extracted from: {url}

Only focus on meaningful visible content — ignore scripts, styles, or metadata.

---

**User Question:** {query}

---

**HTML Content (partial):** {content}

---

**Instructions:**
- Extract and understand relevant visible content (e.g., headings, paragraphs, and lists).
- Answer the user's question clearly and completely.
- If appropriate, structure the output using:
  - Bullet points
  - Headings
  - Tables (e.g., for pros and cons)
- Be concise, informative, and avoid repeating the question.

Provide a complete and well-structured response.
"""

        # Generate content using the Gemini model
        response = model.generate_content(prompt)
        return jsonify({
            'success': True,
            'result': response.text
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
o