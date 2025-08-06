from flask import Flask, render_template, request, jsonify
import os
import time
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

<<<<<<< HEAD

# Initialize Flask app
=======
>>>>>>> e956cda58c79b97f7354783e7c305275712eb882
app = Flask(__name__)
app.config['APP_NAME'] = 'WebSage'

load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

<<<<<<< HEAD
def scrapeweb(url, use_js=False):
    """
    Advanced web scraping function that can bypass robot detection.
    Uses multiple techniques including:
    - Advanced headers and user agent rotation
    - Session management
    - Proxy support
    - JavaScript rendering
    - Rate limiting and retry logic
    """
    import random
    import time
    from datetime import datetime
    import json
    
    # List of user agents to rotate through
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
    ]
    
    # Basic headers
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    # Add referer if available
    if '://' in url:
        headers['Referer'] = url
    
    # Create a session
    session = requests.Session()
    
    # Add cookies to simulate browser behavior
    session.cookies.set('visited', '1', domain=url.split('/')[2])
    
    # Add retry logic
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            # Add random delay between requests
            time.sleep(random.uniform(0.5, 2))
            
            if use_js:
                # Use Selenium for JavaScript rendering
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(url)
                    
                    # Wait for dynamic content to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'body'))
                    )
                    
                    # Get the page content
                    content = driver.page_source
                    driver.quit()
                    
                except Exception as e:
                    return f"Error with Selenium: {str(e)}"
            else:
                # Use requests for regular scraping
                response = session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                content = response.text
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove scripts and styles for cleaner content
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Return cleaned content
            return soup.prettify()[:25000]
            
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                return f"Error scraping {url}: {str(e)}"
            time.sleep(retry_delay * (attempt + 1))
            
    return f"Failed to scrape {url} after {max_retries} attempts"
    
=======
def scrapeweb(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.prettify()[:25000]  # limit size
    except requests.RequestException as e:
        return f"Error scraping {url}: {str(e)}"

>>>>>>> e956cda58c79b97f7354783e7c305275712eb882
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        start_time = time.time()

        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        url = data.get('url')
        query = data.get('query')

        if not url or not query:
            return jsonify({'success': False, 'error': 'URL and query are required'}), 400

        content = scrapeweb(url)
        if content.startswith('Error scraping'):
            return jsonify({'success': False, 'error': content}), 400

        prompt = f"""
You are an expert web content analyst.

Analyze the following HTML content extracted from: {url}

Ignore scripts, styles, metadata. Only focus on visible, meaningful text.

User Question: {query}

HTML Content (partial): {content}

Instructions:
- Answer based only on the page content.
- Use bullet points, headings, or tables when helpful.
- Be concise and clear.
"""

        ai_response = model.generate_content(prompt)
        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        return jsonify({
            'success': True,
            'result': ai_response.text,
            'time_taken': elapsed
        })

    except Exception as e:
<<<<<<< HEAD
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
=======
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> e956cda58c79b97f7354783e7c305275712eb882
