import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") 
SUPABASE_KEY = os.getenv("SUPABASE_KEY") #anon,public key
SUPABASE_REDIRECT_PATH = os.getenv("SUPABASE_REDIRECT_PATH") #callback for OAuth


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)