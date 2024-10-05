import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from typing import List, Dict
from datetime import datetime

def scrape_events(url: str) -> List[Dict[str, str]]:
    try:
        # Make a request to the provided URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the concert list container
        concert_list = soup.find('div', class_='concertslist_page events events_count_3')
        
        # Check if the concert list exists
        if not concert_list:
            print("No events found on the page")
            return []

        events = concert_list.find_all('a', href=True)  # Find all anchor tags with href
        
        results = []
        # Loop through each event
        for idx, event in enumerate(events, start=0):
            article_link = event['href']
            full_article_link = requests.compat.urljoin(url, article_link)  # Build full URL
            
            # Request each article page
            article_page = requests.get(full_article_link)
            article_page.raise_for_status()
            article_page_soup = BeautifulSoup(article_page.text, 'html.parser')

            # Extract title
            article_title = article_page_soup.find('h1')
            if article_title:
                article_title = article_title.get_text(strip=True)
            else:
                article_title = "No title available"

            # Extract description
            article_description = article_page_soup.find('div', class_='concert_details_description_description_inner')
            if article_description:
                article_description_text = article_description.get_text(strip=True)

                # Split description into sentences and filter out unwanted URLs
                sentences = re.split(r'(?<=[.!?])\s+', article_description_text)
                clean_sentences = [
                    sentence for sentence in sentences 
                    if not re.search(r'(http[s]?://\S+|www\.\S+)', sentence)
                ]
                clean_description = ' '.join(clean_sentences)
            else:
                clean_description = "No description available"

            # **Extract location**
            location_tag = article_page_soup.find('a', class_='info_sidebar_component_content_title')
            if location_tag:
                location = location_tag.get_text(strip=True)
            else:
                location = "No location available"

            # Extract detailed location if available
            venue_link_tag = article_page_soup.find('a', class_='info_sidebar_component_content_title')
            
            if venue_link_tag:
                venue_page_url = venue_link_tag['href']
                
                # Now fetch the venue page
                venue_response = requests.get(venue_page_url)
                if venue_response.status_code == 200:
                    venue_soup = BeautifulSoup(venue_response.content, 'html.parser')
                    # Find the span that contains the location details
                    location_details = venue_soup.find_all('span', class_='venue_details_location_detail')
                    # Concatenate the location details into a full address string
                    if location_details:
                        detailed_location = " ".join([detail.get_text(strip=True) for detail in location_details if detail.get_text(strip=True)])
                        location = detailed_location if detailed_location else location

            # **Extract event time**
            event_datetime = None  # Initialize event_datetime as None
            # Find the relevant tag that contains the time details
            time_tag = article_page_soup.find('div', class_='concert_details_spec_content')
            
            if time_tag:
                # Extract the date part
                date_match = re.search(r'\d{2}/\d{2}/\d{4}', time_tag.get_text())
                
                # Extract the time from the span with class 'concert_details_date_time'
                time_tag_span = time_tag.find('span', class_='concert_details_date_time')
                
                if date_match and time_tag_span:
                    event_date = date_match.group()  # Extracts the date in 'dd/mm/yyyy' format
                    event_time = time_tag_span.get_text(strip=True)  # Extracts the time (e.g., '19:00')
                    
                    # Combine date and time into a single datetime object
                    event_datetime_str = f"{event_date} {event_time}"
                    dt = datetime.strptime(event_datetime_str, '%d/%m/%Y %H:%M')
                    event_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
                    
            # Append the cleaned event data to results
            results.append({
                'title': article_title,
                'description': clean_description,
                'link': full_article_link,
                'location': location,
                'event_time': event_datetime  # event_time is either the datetime or None
            })

        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during scraping: {str(e)}")
        return []

    
if __name__ == '__main__':
    url = 'https://www.piletilevi.ee/eng/tickets/koik/'
    events = scrape_events(url)
    for event in events:
        print(event)
