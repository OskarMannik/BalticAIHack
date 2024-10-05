<<<<<<< HEAD
import requests
from llm import CategoryClassifier
from typing import List, Tuple, Dict

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
    """
    This function takes a classification dictionary, a database of companies (with multiple categories),
    and a threshold. It returns the names of companies where any of their categories have a probability
    above the given threshold. The result includes the company name and the highest relevant probability.
    """
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

# Function to process event descriptions from the /scrape endpoint
def process_scrape_data(scrape_url: str, threshold: float):
    # Fetch data from the /scrape endpoint
    response = requests.get(scrape_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        events = response.json()  # Assume the endpoint returns JSON data
        
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
            
            # Output the results for each event
            print(f"Companies with probabilities >= {threshold}:")
            for company, probability in matching_companies:
                print(f"{company}: {probability}")
            
            print("="*50)  # Separator between events
    else:
        print(f"Failed to fetch data from {scrape_url}. Status code: {response.status_code}")

# Example usage
scrape_url = "http://127.0.0.1:5000/scrape"
threshold = 0.3

# Process the event descriptions from the /scrape endpoint
process_scrape_data(scrape_url, threshold)
=======
import requests
from llm import CategoryClassifier
from typing import List, Tuple, Dict

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
    """
    This function takes a classification dictionary, a database of companies (with multiple categories),
    and a threshold. It returns the names of companies where any of their categories have a probability
    above the given threshold. The result includes the company name and the highest relevant probability.
    """
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

# Function to process event descriptions from the /scrape endpoint
def process_scrape_data(scrape_url: str, threshold: float):
    # Fetch data from the /scrape endpoint
    response = requests.get(scrape_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        events = response.json()  # Assume the endpoint returns JSON data
        
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
            
            # Output the results for each event
            print(f"Companies with probabilities >= {threshold}:")
            for company, probability in matching_companies:
                print(f"{company}: {probability}")
            
            print("="*50)  # Separator between events
    else:
        print(f"Failed to fetch data from {scrape_url}. Status code: {response.status_code}")

# Example usage
scrape_url = "http://127.0.0.1:5000/scrape"
threshold = 0.3

# Process the event descriptions from the /scrape endpoint
process_scrape_data(scrape_url, threshold)
>>>>>>> 42c737d6877248e94de836067f917b6e630ed95c
