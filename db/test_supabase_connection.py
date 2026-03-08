import os
from supabase_client import supabase

def test_connection():
    try:
        response = supabase.table('batch_table').select('*').limit(1).execute()
        print("Connection successful:", response.data)
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()
