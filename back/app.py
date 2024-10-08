import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from llm import CategoryClassifier
from typing import List, Tuple, Dict

from supabase import create_client, Client
from datetime import datetime


supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)

# Define the restaurant categories
categories = ['takeout', 'vegetarian', 'casual dining', 'fast food', 'japanese', 'outdoor dining', 'steakhouse', 'rooftop', 'italian', 'fine dining', 'burger', 'vegan', 'sushi', 'organic', 'seafood']


# Initialize the classifier with a translation function (if necessary)
classifier = CategoryClassifier(category_list=categories, threshold=0.0)

# Function to find companies with probabilities above the given threshold
def find_companies_with_probabilities_above_threshold(
    classification: Dict[str, float],
    threshold: float
) -> List[Tuple[int, str, float]]:
    matching_companies = []

    try:
        # Fetch all companies and their categories
        response = supabase.rpc('get_companies_with_categories').execute()
        companies = response.data

        for company in companies:
            company_id = company['id']
            company_name = company['name']
            company_categories = company['categories']  # List of category names

            relevant_probabilities = []
            for category in company_categories:
                if category in classification and classification[category] >= threshold:
                    relevant_probabilities.append(classification[category])

            if relevant_probabilities:
                max_probability = max(relevant_probabilities)
                matching_companies.append((company_id, company_name, max_probability))

    except Exception as e:
        print(f"Exception occurred while fetching companies: {e}")
        # Optionally, you can log the exception or handle it as needed

    return matching_companies





# Function to scrape events
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
                    event_datetime = dt  # Keep as datetime object
                    
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


# Route to scrape events
@app.route('/scrape', methods=['GET'])
def scrape_titles():
    # Get the URL from query params or default to Piletilevi's "all events" page
    url = request.args.get('url', default='https://www.piletilevi.ee/eng/tickets/koik/', type=str)

    events = scrape_events(url)
    if events:
        return jsonify(events)
    else:
        return jsonify({"error": "No events found or an error occurred during scraping."}), 404

# Route to process and classify scraped events
# Route to process and classify scraped events
@app.route('/process_events', methods=['GET'])
def process_events():
    threshold = request.args.get('threshold', default=0.3, type=float)
    url = request.args.get('url', default='https://www.piletilevi.ee/eng/tickets/koik/', type=str)

    events = scrape_events(url)

    all_results = []
    for event in events:
        title = event['title']
        description = event['description']
        link = event['link']
        location = event['location']
        event_time = event['event_time']

        print(f"Processing event: {title}")

        # Classify the description using the CategoryClassifier
        classification = classifier.get_probabilities(description)
        print(f"Classification Results: {classification}")

        # Find matching companies based on the classification
        matching_companies = find_companies_with_probabilities_above_threshold(
            classification, threshold
        )

        # **Print matching companies**
        if matching_companies:
            print("Matching Companies:")
            for _, company_name, probability in matching_companies:
                print(f" - {company_name}: {probability}")
        else:
            print("No matching companies found.")

        # Insert event into the database
        event_data = {
            'title': title,
            'description': description,
            'link': link,
            'location': location,
            'event_time': event_time.isoformat() if event_time else None  # Convert datetime to string
        }

        try:
            response = supabase.table('events').insert(event_data).execute()
            event_id = response.data[0]['id']
        except Exception as e:
            print(f"Error inserting event: {e}")
            continue  # Skip to the next event

        # Insert matches into the database
        if matching_companies:
            match_records = []
            for company_id, _, probability in matching_companies:
                match_records.append({
                    'event_id': event_id,
                    'company_id': company_id,
                    'probability': probability
                })
            try:
                response = supabase.table('event_company_matches').insert(match_records).execute()
            except Exception as e:
                print(f"Error inserting matches: {e}")

        # Prepare the result for this event
        event_result = {
            'event': event,
            'matching_companies': [
                {'company': company_name, 'probability': probability}
                for _, company_name, probability in matching_companies
            ]
        }

        all_results.append(event_result)
        print("=" * 50)  # Separator between events

    return jsonify(all_results)



# Route to classify a single event description
@app.route('/classify', methods=['POST'])
def classify_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON data expected"}), 400

    description = data.get('description', '')
    threshold = data.get('threshold', 0.3)  # Default threshold

    # Validate inputs
    if not description:
        return jsonify({"error": "Description field is required"}), 400

    # Classify the description using the CategoryClassifier
    classification = classifier.get_probabilities(description)
    print(f"Classification Results: {classification}")

    # Find matching companies based on the classification
    matching_companies = find_companies_with_probabilities_above_threshold(
        classification, threshold
    )

    # **Print matching companies**
    if matching_companies:
        print("Matching Companies:")
        for _, company_name, probability in matching_companies:
            print(f" - {company_name}: {probability}")
    else:
        print("No matching companies found.")

    # Prepare the response
    results = [
        {'company': company_name, 'probability': probability}
        for _, company_name, probability in matching_companies
    ]

    return jsonify({'matching_companies': results})

@app.route('/event/<int:event_id>/companies', methods=['GET'])
def get_companies_for_event(event_id):
    # Fetch event details
    try:
        response = supabase.table('events').select('*').eq('id', event_id).execute()
        event_data = response.data
        if not event_data:
            return jsonify({"error": "Event not found"}), 404
        event = event_data[0]
    except Exception as e:
        print(f"Error fetching event: {e}")
        return jsonify({"error": "Error fetching event"}), 500

    # Fetch matching companies
    try:
        response = supabase.rpc('get_event_companies', {'event_id_input': event_id}).execute()
        matching_companies = response.data
    except Exception as e:
        print(f"Error fetching matching companies: {e}")
        return jsonify({"error": "Error fetching matching companies"}), 500

    return jsonify({
        'event': event,
        'matching_companies': matching_companies
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    
