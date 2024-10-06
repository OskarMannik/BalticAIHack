from supabase import create_client, Client
import random  # Import random module to generate random numbers

# Initialize Supabase client
supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)

# Function to update the distance column with random values between 0 and 50
def update_distance_with_random_numbers():
    try:
        # Fetch data from the 'event_company_matches' table
        response = supabase.table('event_company_matches').select('company_id', 'event_id').execute()
        
        # Iterate over the response data
        for match in response.data:
            company_id = match['company_id']
            event_id = match['event_id']
            
            # Generate a random number between 0 and 50
            random_distance = random.randint(0, 20)
            
            # Update the 'distance' column in the 'event_company_matches' table with the random numbe
            
            update_response = supabase.table('event_company_matches')\
                .update({'distance': random_distance})\
                .eq('company_id', company_id)\
                .eq('event_id', event_id)\
                .execute()
            
            # Print the update confirmation for each row
            print(f"Updated distance for company_id {company_id} and event_id {event_id}: {random_distance}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
update_distance_with_random_numbers()
