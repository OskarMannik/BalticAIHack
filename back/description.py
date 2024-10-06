import os
from supabase import create_client, Client
from groq import Groq

# Initialize Supabase client
supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)

# Initialize LLM client (Groq)
api_key = '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'  # Replace with your actual Groq API key
client = Groq(api_key=api_key)
model_name = 'llama-3.1-8b-instant'  # Or the appropriate model

def generate_llm_description(event_description):
    # Build the prompt
    prompt = (
        "You are a market analyst specialized in the restaurant industry. "
        "Given the following event description, provide an analysis on how restaurants could benefit from this event, "
        "including an estimation of how many customers they might expect. "
        "Event Description: "
        f"{event_description}\n"
        "Please provide your analysis."
    )
    try:
        # Send request to the LLM
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that provides market analysis for restaurants."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model=model_name,
        )
        # Extract the response
        llm_description = response.choices[0].message.content.strip()
        return llm_description
    except Exception as e:
        print(f"Error generating LLM description: {e}")
        return None

def main():
    # Fetch events from the database
    try:
        response = supabase.table('events').select('*').execute()
        events = response.data
        for event in events:
            event_id = event['id']
            event_description = event['description']
            # Check if the event already has an llm_description
            if event.get('llm_description'):
                print(f"Event {event_id} already has an LLM description. Skipping.")
                continue
            # Generate LLM description
            llm_description = generate_llm_description(event_description)
            if llm_description:
                # Update the event in the database
                supabase.table('events').update({'llm_description': llm_description}).eq('id', event_id).execute()
                #print(llm_description)
                print(f"Updated event {event_id} with LLM description.")
            else:
                print(f"Skipping event {event_id} due to error in LLM generation.")
    except Exception as e:
        print(f"Error fetching events: {e}")

if __name__ == '__main__':
    main()
