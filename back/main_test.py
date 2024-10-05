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
classifier = CategoryClassifier(category_list=categories, threshold=0.2)

# Sample text, which could be in English or Estonian
text_to_classify = (
    "Tallinn, pane end valmis! 9. juunil 2025 jõuab oma maailmaturnee raames Tallinna Lauluväljakule globaalne superstaar Justin Timberlake. Albumi “Everything I Thought It Was” tuules esmakordselt Eestisse saabuv Timberlake on taas lavadel pärast viieaastast pausi. See on sündmus, millest Eesti muusikasõbrad kindlasti ilma ei taha jääda! Tennessee osariigis Memphises sündinud Timberlake on veetnud suurema osa oma elust tähelepanu keskpunktis. Hea esinemisoskus avaldus juba noorena, kui ta astus üles kohalikes populaarsetes telesaadetes nagu Star Search ja The Mickey Mouse Club, kus ta jagas lava teiste tulevaste staaridega, näiteks Britney Spearsi ja Christina Aguileraga. Timberlake’i tõeline tähelend algas aga 1990ndate lõpus koos poistebändiga NSYNC, mis on müünud maailmas üle 70 miljoni plaadi ning jätnud popkultuuri tugeva jälje."
)

text_to_classify_translated = classifier.translate_to_english(text_to_classify)
print(text_to_classify_translated)

# Classify the translated text and get probabilities
classification = classifier.get_probabilities(text_to_classify_translated)

# Print the classification results
print("Classification Results:", classification)

# Define a sample company database with company names and categories
database = [
    ("Burger World", "fast food"),
    ("Sushi Heaven", "sushi"),
    ("Steak House", "steakhouse"),
    ("Green Delight", "vegan"),
    ("Pizza Palace", "italian"),
    ("Seafood Shack", "seafood"),
]

# Function to find companies with probabilities above the given threshold
def find_companies_with_probabilities_above_threshold(
    classification: Dict[str, float],
    database: List[Tuple[str, str]],
    threshold: float
) -> List[str]:
    """
    This function takes a classification dictionary, a database of companies, and a threshold.
    It returns the names of companies where the category's probability is above the given threshold.
    """
    matching_companies = []

    # Loop through the database and match categories with probabilities from the classification
    for company, category in database:
        # Check if the category exists in the classification dictionary
        if category in classification:
            # Check if the probability for that category is above the threshold
            if classification[category] >= threshold:
                matching_companies.append(company)

    return matching_companies

# Example usage: Find companies with probabilities >= 0.3
threshold = 0.5
matching_companies = find_companies_with_probabilities_above_threshold(classification, database, threshold)

# Print the companies that match the threshold
print("Companies with probabilities >= 0.3:", matching_companies)
