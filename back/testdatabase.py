from supabase import create_client, Client

supabase_url = 'https://vgxifmuuonfxuwoperyd.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneGlmbXV1b25meHV3b3BlcnlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODA3MDQzNSwiZXhwIjoyMDQzNjQ2NDM1fQ.jvuAV0rQrjnn8W0ANZOxfgO1B8Hsqx2FENu6X5myE7Q'

supabase: Client = create_client(supabase_url, supabase_key)

def populate_companies():
    # Define your companies and their categories
    company_data = [
        ("Burger World", ["fast food", "burger", "casual dining"]),
        ("Sushi Heaven", ["sushi", "japanese", "fine dining"]),
        ("Steak House", ["steakhouse", "fine dining", "rooftop"]),
        ("Green Delight", ["vegan", "vegetarian", "organic"]),
        ("Pizza Palace", ["italian", "casual dining", "takeout"]),
        ("Seafood Shack", ["seafood", "fine dining", "outdoor dining"]),
    ]

    # Insert categories using upsert to handle duplicates
    categories_set = {cat for _, cats in company_data for cat in cats}
    categories_list = [{'name': category} for category in categories_set]
    supabase.table('categories').upsert(categories_list, on_conflict='name').execute()

    # Get category IDs
    response = supabase.table('categories').select('id, name').execute()
    categories = response.data
    category_id_map = {item['name']: item['id'] for item in categories}

    # Insert companies using upsert to handle duplicates
    companies_list = [{'name': company_name} for company_name, _ in company_data]
    supabase.table('companies').upsert(companies_list, on_conflict='name').execute()

    # Get company IDs
    response = supabase.table('companies').select('id, name').execute()
    companies = response.data
    company_id_map = {item['name']: item['id'] for item in companies}

    # Prepare data for company_category table
    company_category_list = []
    for company_name, category_list in company_data:
        company_id = company_id_map[company_name]
        for category_name in category_list:
            category_id = category_id_map[category_name]
            company_category_list.append({
                'company_id': company_id,
                'category_id': category_id
            })

    # Insert into company_category using upsert to handle duplicates
    supabase.table('company_category').upsert(company_category_list, on_conflict='company_id,category_id').execute()

    print("Companies and categories populated.")

if __name__ == '__main__':
    populate_companies()
