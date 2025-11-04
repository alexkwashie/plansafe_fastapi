from dotenv import load_dotenv
from supabase import create_client
import os

# Load .env file (for local development)
load_dotenv()

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Basic validation
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

# Create Supabase client (URL first, then key)
auth_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)