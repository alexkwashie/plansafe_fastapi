import os
from supabase_client import supabase

def test_connection():
    try:
        # Replace 'your_table_name' with an actual table name in your Supabase database
        response = supabase.table('users').select('*').limit(1).execute()
        print("Connection successful:", response.data)
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()
