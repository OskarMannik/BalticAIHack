import os
import re
from groq import Groq

# Define the simplified CategoryClassifier class
class CategoryClassifier():
    def __init__(self, category_list, api_key=None, model_name="llama-3.1-8b-instant", threshold=0.0):
        # Initialize the Groq API client
        self.api_key = "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"  # use your actual API key here
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        self.category_list = category_list
        self.threshold = threshold

    def get_probabilities(self, text):
        """
        Classifies the text into categories with probabilities using the Groq API.
        This is the core functionality that can be exposed for external use.
        """
        # Send request to the Groq API with user input text and predefined categories
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI model specialized in predicting market trends for the restaurant industry. Given an event description, "
                        "your task is to analyze the event and determine which types of restaurants are most likely to benefit from the event. "
                        "Specifically, classify the event into the following restaurant categories and predict the likelihood (between 0 and 1) "
                        "that each category will experience an increase in demand due to the event. The categories are: "
                        f"{str(self.category_list)}. "
                        "Each category should have an independent probability, and the probabilities do not need to sum to 1. "
                        "Respond **only** with a dictionary in this format: {<category>: <probability>, <category>: <probability>, ...}. "
                        "Do not provide any explanations, just the dictionary output."
                    )
                },
                {
                    "role": "user",
                    "content": text,  # The event description goes here
                }
            ],
            model=self.model_name,
        )

        # Process the response from the model
        response_text = response.choices[0].message.content.strip()
        classification_results = {}

        # Split the response by commas to get each category-probability pair
        categories_probabilities = response_text.split(",")

        for category_probability in categories_probabilities:
            try:
                # Split each pair into category and probability
                category, probability = category_probability.split(":")
                # Clean the probability string by removing non-numeric characters
                probability = re.sub(r'[^\d.]', '', probability)
                probability_value = float(probability.strip())

                # Clean the category by removing any quotes (' or ") and extra spaces
                cleaned_category = category.strip("'\" ").lower()  # Remove quotes and spaces, make it lowercase

                # Only add categories with probability greater than the threshold
                if probability_value > self.threshold:
                    classification_results[cleaned_category] = probability_value

            except ValueError:
                # Handle case where the response format is not as expected
                continue

        return classification_results
