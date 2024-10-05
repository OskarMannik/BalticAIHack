import os
import re
from groq import Groq

# Define the simplified CategoryClassifier class
class CategoryClassifier():
    def __init__(self, category_list, api_key=None, model_name="llama-3.1-8b-instant", threshold=0.0):
        # Initialize the Groq API client
        self.api_key ="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" #api_key if api_key else os.environ.get("../../GROQ_API_KEY")
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
                        "You are an AI model designed to analyze events and predict how they will impact various industries or business services. "
                        "Given a specific event description, your task is to assess the likelihood of increased demand for specific business services or industries "
                        "and provide an independent probability score (between 0 and 1) for each of the following categories: "
                        f"{str(self.category_list)}. "
                        "Each probability should reflect how likely it is that the corresponding business or service will experience an increase in demand based on the event described. "
                        "Each probability should be independent of the others, and the sum of probabilities across categories does not need to equal 1. "
                        "Please provide your response in the following format, and only in this format: <category>: <probability>, <category>: <probability>, ... "
                        "Ensure the probabilities are formatted as numbers between 0 and 1, and that they correspond to each category. "
                        "Do not provide any additional information or text beyond the category names and their probabilities."
                    )
                },
                {
                    "role": "user",
                    "content": text,  # The text that needs classification
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

                # Only add categories with probability greater than the threshold
                if probability_value > self.threshold:
                    classification_results[category.strip()] = probability_value

            except ValueError:
                # Handle case where the response format is not as expected
                continue

        return classification_results