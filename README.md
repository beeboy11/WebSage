# WebSage 🌐

An AI-powered web scraping and analysis tool using Google's Gemini AI.

## Features

- 🤖 AI-powered content analysis using Gemini Pro
- 🌐 Intelligent web scraping capabilities
- 💬 Natural language querying of web content
- ⚡ Real-time processing and response
- 🎨 Clean, modern user interface

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/websage.git
cd websage
```

2. Create a virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the project root and add:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Usage

1. Start the server:
```bash
python flasksetup.py
```

2. Open your browser and visit `http://localhost:5000`
3. Enter a website URL and your question
4. Get AI-powered analysis of the web content

## Tech Stack

- Flask
- Google Gemini AI
- BeautifulSoup4
- JavaScript
- HTML/CSS

## License

MIT

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
