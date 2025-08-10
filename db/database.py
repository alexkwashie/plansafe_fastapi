from db.supabase_client import supabase

def get_db():
    yield supabase
