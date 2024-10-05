from llm import CategoryClassifier
from typing import List, Tuple, Dict

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
    
# Initialize the classifier
classifier = CategoryClassifier(category_list=categories, threshold=0.2)
    
    # Classify a sample text
text_to_classify = "At the beginning of December 2024, the Vienna Strauss Philharmonie Orchestra will perform for the third time  in its history - after last year’s incredible success! - will tour Estonia and give concerts in Pärnu (05.12.) Tartu (06.12.)  Tallinn (07.12) Jõhvi (8.12) The group will perform a NEW program, which includes works by Mozart, Brahms, Haydn, Albinoni, Bach, the brilliant Kalman and, of course, the Strauss dynasty. The orchestra was created in 2014 by the founder of the world famous Mozart Orchestra, Gerald Grünbacher (Vienna, Austria) The Orchestra's conductor is András Deák, a talented, charismatic maestro with a long, successful career. 27 musicians from all over the world (Austria, Hungary, Japan, Ukraine, Germany, Poland, Taiwan, Croatia, Cyprus) were selected by a special jury for this tour. The group's activities are aimed at preserving and developing the musical culture of Vienna and promoting it at the European and international level. Chief conductor Andras Laszlo Deak, a recognized maestro and brilliant conductor, will perform two full parts with incredible energy. András Deák has performed in many famous concert halls with the world's leading orchestras: with the Calgary Philharmonic Orchestra (Canada) at Jack Singers Hall (Calgary); at the Orpheum Theater in Vancouver with the Vancouver Opera Orchestra; at the Kennedy Center in Washington with the Baltimore Symphony Orchestra; in Chicago with the orchestra of the famous Chicago Lyric Opera. In 2006, András László Deak was invited to the Vienna Musikverein as conductor of the Vienna Mozart Orchestra and has since become a permanent guest conductor of this famous ensemble. The organizers hope that this evening will INSPIRE you and give you UNFORGETTABLE JOYFUL EMOTIONS."

classification = classifier.get_probabilities(text_to_classify)
    
    # Print the results
print(classification)

database = [
    ("Burger World", "fast food"),
    ("Sushi Heaven", "sushi"),
    ("Steak House", "steakhouse"),
    ("Green Delight", "vegan"),
    ("Pizza Palace", "italian"),
    ("Seafood Shack", "seafood"),
]

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
threshold = 0.3
matching_companies = find_companies_with_probabilities_above_threshold(classification, database, threshold)

# Print the results
print("Companies with probabilities >= 0.3:")
print(matching_companies)