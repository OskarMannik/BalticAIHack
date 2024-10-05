from llm import CategoryClassifier
from typing import List, Tuple, Dict

# Define the restaurant categories
categories = [
    "fast food",
    "food truck",
    "casual dining",
    "fine dining",
    "takeout",
    "italian",
    "chinese",
    "japanese",
    "thai",
    "sushi",
    "steakhouse",
    "burger",
    "seafood",
    "vegan",
    "vegetarian",
    "romantic",
    "rooftop",
    "sports bar",
    "outdoor dining",
    "breakfast",
    "café",
    "wine"
]

# Initialize the classifier with a translation function
classifier = CategoryClassifier(category_list=categories, threshold=0.0)

# Sample text, which could be in English or Estonian
text_to_classify = (
    "Sat, 5 October 17.00 Heino Eller Music School, Tubin Hall Better than Brahms? Concert and conversation panel Tõnu Kalm (clarinet) Mihhail Gerts (piano) Age Juurikas (piano) Programme: Brahms. Clarinet sonata no 1 in F minor op. 120/1 Tubin. Piano sonata no 1 in E major ETW 31 Tubin is a genius. He is better than Brahms, better than me, and certainly better than Eller, said Artur Kapp about Tubin. To unravel this statement, Joonas Hellerma will be joined in conversation by composers Rasmus Puur and Erkki-Sven Tüür. Together, we will find out if this is true. The concert presents Johannes Brahms' first clarinet sonata and Eduard Tubin's first piano sonata. Performed by Tõnu Kalm, Mihhail Gerts and Age Juurikas."
)

#text_to_classify_translated = classifier.translate_to_english(text_to_classify)
#print(text_to_classify_translated)

# Classify the translated text and get probabilities
classification = classifier.get_probabilities(text_to_classify)#should be text_to_classify_translated

# Print the classification results
print("Classification Results:", classification)

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
    database: List[Tuple[str, List[str]]],  # Changed to handle a list of categories for each company
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

# Example usage: Find companies with probabilities >= 0.3

# Example usage: Find companies with any relevant category probabilities >= 0.5
threshold = 0.3
matching_companies = find_companies_with_probabilities_above_threshold(classification, database, threshold)

# Print the results
print("Companies with probabilities >= 0.3:")
for company, probability in matching_companies:
    print(f"{company}: {probability}")

