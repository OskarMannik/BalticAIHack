from llm import CategoryClassifier

categories = ['transportation', 'catering', 'customer service', 'security']
    
# Initialize the classifier
classifier = CategoryClassifier(category_list=categories, threshold=0.1)
    
    # Classify a sample text
text_to_classify = "Join us for our annual company retreat on November 15th at the Lakeside Resort. Activities include team-building exercises, workshops, and a gala dinner."
classification = classifier.get_probabilities(text_to_classify)
    
    # Print the results
print("Classification Results:", classification)