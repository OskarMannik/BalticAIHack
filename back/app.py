import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
from llm import CategoryClassifier
from typing import List, Tuple, Dict

app = Flask(__name__)

# Define the restaurant categories
categories = [
    "fast food", "food truck", "casual dining", "fine dining", "takeout",
    "italian", "chinese", "japanese", "thai", "sushi", "steakhouse", "burger",
    "seafood", "vegan", "vegetarian", "romantic", "rooftop", "sports bar",
    "outdoor dining", "breakfast", "café", "wine"
]

# Initialize the classifier with a translation function (if necessary)
classifier = CategoryClassifier(category_list=categories, threshold=0.0)

# Define a sample company database with company names and categories
database = [
    ("Burger World", ["fast food", "burger", "casual dining"]),
    ("Sushi Heaven", ["sushi", "japanese", "fine dining"]),
    ("Steak House", ["steakhouse", "fine dining", "rooftop"]),
    ("Green Delight", ["vegan", "vegetarian", "organic"]),
    ("Pizza Palace", ["italian", "casual dining", "takeout"]),
    ("Seafood Shack", ["seafood", "fine dining", "outdoor dining"]),
]

# Function to find companies with probabilities above the given threshold
def find_companies_with_probabilities_above_threshold(
    classification: Dict[str, float],
    database: List[Tuple[str, List[str]]],  # Companies have multiple categories
    threshold: float
) -> List[Tuple[str, float]]:
    matching_companies = []

    # Loop through the database, where each company has multiple categories
    for company, categories in database:
        # Initialize a list to store probabilities for this company's categories
        relevant_probabilities = []

        # Loop through the company's categories
        for category in categories:
            # Check if the category exists in the classification dictionary
            if category in classification:
                # Check if the probability for that category is above the threshold
                if classification[category] >= threshold:
                    relevant_probabilities.append(classification[category])

        # If the company has relevant categories, calculate relevance (e.g., max probability)
        if relevant_probabilities:
            max_probability = max(relevant_probabilities)  # Using max probability for simplicity
            matching_companies.append((company, max_probability))

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

            # Append the cleaned event data to results
            results.append({
                'title': article_title,
                'description': clean_description,
                'link': full_article_link
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

        print(f"Processing event: {title}")

        # Classify the description using the CategoryClassifier
        classification = classifier.get_probabilities(description)
        print(f"Classification Results: {classification}")

        # Find matching companies based on the classification
        matching_companies = find_companies_with_probabilities_above_threshold(
            classification, database, threshold
        )

        # Prepare the result for this event
        event_result = {
            'event': event,
            'matching_companies': [
                {'company': company, 'probability': probability}
                for company, probability in matching_companies
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
    translated_desc = classifier.translate_to_english(description)#TEXT RANSLATION !!!!
    classification = classifier.get_probabilities(translated_desc)#CLASSIFYING THE TEXT !!!!
    print(f"Classification Results: {classification}")

    # Find matching companies based on the classification
    matching_companies = find_companies_with_probabilities_above_threshold(
        classification, database, threshold
    )

    # Prepare the response
    results = [
        {'company': company, 'probability': probability}
        for company, probability in matching_companies
    ]

    return jsonify({'matching_companies': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    
