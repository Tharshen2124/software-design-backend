import os
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions
from .supabase_storage import AppSessionStorage

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") 
SUPABASE_KEY = os.getenv("SUPABASE_KEY") #anon,public key
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") #anon,public key
SUPABASE_REDIRECT_PATH = os.getenv("SUPABASE_REDIRECT_PATH") #callback for OAuth

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_supabase(request) -> Client:
    storage = AppSessionStorage(request.session)
    options = ClientOptions(
        storage=storage,
        flow_type='pkce' 
    )
    return create_client(SUPABASE_URL, SUPABASE_KEY, options)