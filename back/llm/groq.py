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
                        f"You are an AI classifier. Classify the following text into the following categories: "
                        f"{str(self.category_list)} and give the probability for each. "
                        "Respond in this format: <category>: <probability>, <category>: <probability>, ..."
                    )
                },
                {
                    "role": "user",
                    "content": text,
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