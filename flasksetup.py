from flask import Flask, render_template, request, jsonify
import os
import time
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = Flask(__name__)
app.config['APP_NAME'] = 'WebSage'

load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

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
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
