from supabase import create_client, Client
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import time
from transformers import GPT2Tokenizer, pipeline

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load a pre-trained summarization model and tokenizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6", device=0 if device == "cuda" else -1)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # Initialize the tokenizer

# Function to summarize the description if it's too long
def summarize_prompt(prompt):
    prompt = "accurate " + prompt  # Prepend "accurate " at the beginning
    
    # Check if the prompt exceeds 77 tokens
    if len(tokenizer.encode(prompt)) > 77:  
        # Summarize the prompt if it's too long
        summary = summarizer(prompt, max_length=60, min_length=30, do_sample=False)[0]['summary_text']
        print(f"Summarized prompt: {summary}")
        return "accurate " + summary  # Ensure "accurate" is added to the summarized prompt
    return prompt

# Supabase credentials
supabase_url = "https://vgxifmuuonfxuwoperyd.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q"

# Initialize the Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Function to get all events from Supabase
def get_all_events():
    response = supabase.table('events').select('id', 'description').execute()
    if response.data:
        return response.data
    else:
        return []

# Load the Stable Diffusion model
def load_model():
    try:
        pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2", torch_dtype=torch.float16)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        pipe = pipe.to(device)  # Use GPU if available, fallback to CPU if not
        return pipe
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
    
# Function to generate the image locally
def generate_image(description, pipe):
    try:
        summarized_description = summarize_prompt(description)
        # Generate the image based on the description
        image = pipe(summarized_description, num_inference_steps=25).images[0]
        return image
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Function to upload image to Supabase storage
def upload_image_to_supabase(image, file_name):
    try:
        # Save the image to a byte stream (in-memory file) as JPG
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        # Upload image to Supabase storage
        file_path = f"diffusion_pictures/{file_name}.jpg"
        response = supabase.storage().from_('diffusion_pictures').upload(file_path, img_byte_arr.read())

        if response:
            print(f"Image {file_name}.jpg uploaded successfully")
            return file_path
        else:
            raise Exception("Failed to upload image to Supabase")
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

# Function to get public URL for uploaded image
def get_image_url(file_path):
    try:
        public_url = supabase.storage().from_('diffusion_pictures').get_public_url(file_path)
        return public_url
    except Exception as e:
        print(f"Error fetching public URL: {e}")
        return None

# Main logic
if __name__ == "__main__":
    # Load the Stable Diffusion model
    pipe = load_model()

    if pipe:  # Proceed if the model is successfully loaded
        events = get_all_events()

        if events:
            print(f"Found {len(events)} events. Generating images...")
            for event in events:
                event_id = event['id']
                description = event['description']
                print(f"Generating image for event {event_id}: '{description}'")

                # Generate image
                image = generate_image(description, pipe)

                if image:
                    # Upload image to Supabase storage
                    file_name = f"event_{event_id}"
                    file_path = upload_image_to_supabase(image, file_name)

                    if file_path:
                        # Get public URL of the uploaded image
                        public_url = get_image_url(file_path)
                        if public_url:
                            print(f"Public URL for event {event_id}: {public_url}")
                        else:
                            print(f"Failed to get public URL for event {event_id}")
                    else:
                        print(f"Failed to upload image for event {event_id}")
                else:
                    print(f"Failed to generate image for event {event_id}")

                # Sleep for a short duration to avoid overwhelming API or system resources
                try:
                    time.sleep(2)  # Sleep to avoid overloading the system
                except Exception as e:
                    print(f"Error with sleep: {e}")
        else:
            print("No events found in the database.")
    else:
        print("Failed to load the Stable Diffusion model.")
