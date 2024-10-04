import requests
from bs4 import BeautifulSoup

def scrape_titles(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('span', class_='event_short_title')
        
        # Extract and print the titles
        for idx, title in enumerate(titles, start=1):
            print(f"{idx}. {title.get_text(strip=True)}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

scrape_titles("https://www.piletilevi.ee/eng/tickets/sport/")
    