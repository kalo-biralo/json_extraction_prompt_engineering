import requests
from bs4 import BeautifulSoup

# Function to fetch Wikipedia page content in HTML format by URL
def fetch_wikipedia_page_by_url(url):
    headers = {
        'User-Agent': 'prompt engineering'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the text content from the HTML, ignoring tables, images, etc.
        paragraphs = soup.find_all('p')
        text_content = '\n\n'.join([para.get_text() for para in paragraphs])
        
        return text_content
    else:
        return None