from supabase import create_client, Client
from geopy.geocoders import Nominatim
from math import radians, cos, sin, sqrt, atan2, acos

# Initialize Supabase client
supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)

# Initialize the geolocator (Nominatim)
geolocator = Nominatim(user_agent="geoapiExercises")

# Haversine formula to calculate distance between two geographic points
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371.0  # Radius of Earth in kilometers
    return r * c / 1000

# Function to get data from the table, geocode event locations, calculate distance, and update the database
def get_distance_to_event():
    try:
        # Fetch data from the 'event_company_matches' table
        response = supabase.table('event_company_matches').select('company_id', 'event_id').execute()
        
        # Iterate over the response data
        for match in response.data:
            company_id = match['company_id']
            event_id = match['event_id']
            
            # Fetch company location based on company_id
            company_lon_lat = supabase.table('companies').select('longitude', 'latitude').eq('id', company_id).execute()
            
            if company_lon_lat.data:
                company_lon = company_lon_lat.data[0]['longitude']
                company_lat = company_lon_lat.data[0]['latitude']
                
            # Fetch event location based on event_id
            event_response = supabase.table('events').select('location').eq('id', event_id).execute()
            
            if event_response.data and event_response.data[0]['location'] is not None:
                event_location = event_response.data[0]['location']
                
                if event_location:
                    event_location_geo = geolocator.geocode(event_location)
                                    
                    event_lat = event_location_geo.latitude
                    event_lon = event_location_geo.longitude
                    print(f"Event ID: {event_id}, Location: {event_location}, Latitude: {event_lat}, Longitude: {event_lon}")
                    
                    # Calculate distance in kilometers and convert to integer
                    distance_km = haversine(company_lon, company_lat, event_lon, event_lat)
                    distance_int = int(distance_km)
                    print(f"Distance (km): {distance_int}")
                    
                    # Update the 'distance' column in the 'event_company_matches' table
                    update_response = supabase.table('event_company_matches').update({'distance': distance_int}).eq('company_id', company_id).eq('event_id', event_id).execute()
                    
                    print(f"Updated distance for company_id {company_id} and event_id {event_id}: {distance_int}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
get_distance_to_event()
