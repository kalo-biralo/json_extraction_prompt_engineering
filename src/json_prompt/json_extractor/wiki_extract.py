import requests
from bs4 import BeautifulSoup

# Function to fetch Wikipedia page content in HTML format by URL
def fetch_wikipedia_page_by_url(url):
    headers = {
        'User-Agent': 'prompt engineering'
    }
    try:
        response = requests.get(url, headers=headers, timeout = 5)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract the text content from the HTML, ignoring tables, images, etc.
            paragraphs = soup.find_all('p')
            text_content = '\n\n'.join([para.get_text() for para in paragraphs])

            if not text_content.strip():
                return ValueError("Fetched content is empty.")
            
            return text_content
        else:
            return ValueError(f"Failed to fetch content, status code: {response.status_code}")
        
    except requests.Timeout:
        return TimeoutError("The request timed out.")
    except requests.RequestException as e:
        return ValueError(f"Request failed: {e}")
    except Exception as e:
        return ValueError(f"An error occured: {e}")
