from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# HTML Template for Home Page
home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dorking Hub - Advanced Search</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
            background: linear-gradient(135deg, #1e90ff, #ff7f50);
        }
        header {
            text-align: center;
            padding: 80px 20px;
            background: #1c1c1c;
            color: white;
        }
        header h1 {
            font-size: 4rem;
            margin-bottom: 15px;
        }
        header p {
            font-size: 1.5rem;
            font-weight: 300;
        }
        nav {
            background: #333;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        nav a {
            color: white;
            text-decoration: none;
            margin: 0 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .search-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .search-container form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .search-container input, .search-container select {
            width: 80%;
            padding: 12px;
            margin: 10px 0;
            font-size: 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .search-container button {
            padding: 12px 25px;
            font-size: 1rem;
            background: #1e90ff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .search-container button:hover {
            background: #104e8b;
        }
        .content-section {
            padding: 30px;
            max-width: 900px;
            margin: 20px auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .content-section h2 {
            color: #1c1c1c;
            margin-bottom: 1rem;
        }
        .content-section ul {
            list-style-type: disc;
            margin-left: 20px;
        }
        .dork-generator {
            text-align: center;
            margin: 30px 0;
            padding: 30px;
            background: #1e1e1e;
            color: white;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
        }
        .dork-generator input {
            width: 80%;
            padding: 12px;
            margin: 10px 0;
            font-size: 1rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #f4f4f9;
            color: #333;
        }
        .dork-generator button {
            padding: 10px 20px;
            background: #1e90ff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }
        .dork-generator button:hover {
            background: #104e8b;
        }
        .dork-generator .result {
            margin-top: 20px;
            padding: 20px;
            background: #f4f4f9;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            color: #333;
        }
        .dork-generator .result a {
            color: #1e90ff;
            text-decoration: none;
            font-weight: bold;
        }
        .dork-generator .result a:hover {
            text-decoration: underline;
        }
        footer {
            background: #1c1c1c;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 30px;
        }
        footer a {
            color: #1e90ff;
            text-decoration: none;
        }
        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="#about">About</a>
        <a href="#features">Features</a>
        <a href="#dork-guide">Dorking Guide</a>
        <a href="#generator">Command Generator</a>
        <a href="#contact">Contact</a>
    </nav>
    <header>
        <h1>Dorking Hub</h1>
        <p>Discover the power of advanced search</p>
    </header>
    <div class="search-container">
        <form action="/search" method="POST">
            <input type="text" name="query" placeholder="Enter your search query (e.g., 'site:example.com')" required>
            <select name="filter">
    <option value="">No Filter</option>
    <option value="intitle:">Title Contains</option>
    <option value="inurl:">URL Contains</option>
    <option value="filetype:">File Type</option>
    <option value="site:">Site Specific</option>
    <option value="intitle:login OR inurl:login">Login Pages</option>
    <option value='"password" OR "passwd" OR "pwd"'>Forgot Passwords</option>
    <option value='intitle:"index of /"'>Directories</option>
    
</select>

            <button type="submit">Search</button>
        </form>
    </div>
    <div class="content-section" id="about">
        <h2>About Dorking Hub</h2>
        <p>Dorking Hub is your ultimate search partner for precision and efficiency. Our platform leverages advanced algorithms to provide tailored results for your queries.</p>
    </div>
    <div class="content-section" id="features">
        <h2>Features</h2>
        <ul>
            <li>Search for specific file types like PDFs, Excel sheets, and more.</li>
            <li>Find images, videos, and multimedia with precision.</li>
            <li>Use advanced filters like <code>intitle</code>, <code>inurl</code>, and <code>site</code>.</li>
            <li>Intuitive design and user-friendly interface.</li>
            <li>Customizable search options to meet your needs.</li>
        </ul>
    </div>
    <div class="content-section" id="dork-guide">
        <h2>Google Dorking Guide</h2>
        <ul>
            <li><strong>site:</strong> Search within a specific site. Example: <code>site:example.com</code></li>
            <li><strong>intitle:</strong> Search for pages with specific words in the title. Example: <code>intitle:"login"</code></li>
            <li><strong>inurl:</strong> Search for pages with specific words in the URL. Example: <code>inurl:"admin"</code></li>
            <li><strong>filetype:</strong> Search for specific file types. Example: <code>filetype:pdf</code></li>
            <li><strong>cache:</strong> View Google's cached version of a page. Example: <code>cache:example.com</code></li>
        </ul>
    </div>
    <div class="dork-generator" id="generator">
        <h2>Google Dork Command Generator</h2>
        <p>Enter your query below, and we’ll generate the perfect Google Dork command for you.</p>
        <form action="/generate" method="POST">
            <input type="text" name="query" placeholder="Enter keywords or domain" required>
            <button type="submit">Generate Command</button>
        </form>
        {% if dork %}
        <div class="result">
            <h3>Generated Command</h3>
            <p><code>{{ dork }}</code></p>
            <button onclick="copyToClipboard('{{ dork }}')">Copy Command</button>
            <a href="https://www.google.com/search?q={{ dork }}" target="_blank">
                <button>Search on Google</button>
            </a>
        </div>
        {% endif %}
    </div>
    <div class="content-section" id="contact">
        <h2>Contact Us</h2>
        <p>Phone: +1-234-567-8910</p>
        <p>Email: support@dorkinghub.com</p>
    </div>
    <footer>
        &copy; 2024 Dorking Hub | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a>
    </footer>
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Dork command copied to clipboard!');
            }, (err) => {
                alert('Failed to copy command.');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_html)

@app.route('/generate', methods=['POST'])
def generate():
    query = request.form.get('query', "").strip()
    dork = f'site:"{query}" intitle:"{query}"'  # Example generation logic for dork code
    return render_template_string(home_html, dork=dork)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', "").strip()
    filter_type = request.form.get('filter', "").strip()
    full_query = query
    if filter_type:
        if filter_type == 'images':
            full_query = f"{query} filetype:jpg OR filetype:png"
        elif filter_type == 'videos':
            full_query = f"{query} filetype:mp4 OR filetype:avi"
        else:
            full_query = f"{query} {filter_type}"

    results = scrape_google(full_query)
    return render_template_string(results_html, query=full_query, results=results)

def scrape_google(query, max_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}&num={max_results}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return [{"error": "Failed to fetch results from Google"}]

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for g in soup.select('.tF2Cxc'):
        title = g.select_one('h3').text if g.select_one('h3') else "No title"
        link = g.select_one('a')['href'] if g.select_one('a') else "No link"
        snippet = g.select_one('.VwiC3b').text if g.select_one('.VwiC3b') else "No snippet"
        results.append({"title": title, "link": link, "snippet": snippet})

    return results

results_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background: #1c1c1c;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .result-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #ddd;
        }
        .result-item img {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .result-content {
            flex-grow: 1;
        }
        .result-item a {
            font-size: 1.1rem;
            color: #1e90ff;
            text-decoration: none;
        }
        .result-item a:hover {
            text-decoration: underline;
        }
        .result-item .url {
            color: #006621;
            font-size: 0.85rem;
        }
        .result-item .snippet {
            font-size: 0.95rem;
            color: #545454;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            color: #555;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>Search Results</h1>
    </header>
    <div class="container">
        <h2>Results for: "{{ query }}"</h2>
        {% if results %}
        <ul>
            {% for item in results %}
            <li class="result-item">
                <div class="result-content">
                    <a href="{{ item['link'] }}" target="_blank">{{ item['title'] }}</a>
                    <div class="url"><a href="{{ item['link'] }}" target="_blank">{{ item['link'] }}</a></div>
                    <div class="snippet">{{ item['snippet'] }}</div>
                </div>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No results found. Try another query.</p>
        {% endif %}
        <a href="/" style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: #1c1c1c; color: white; border-radius: 5px; text-decoration: none;">Back to Home</a>
    </div>
    <footer>
        &copy; 2025 Dorking Hub by Isra Abass | All Rights Reserved
    </footer>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)      
    