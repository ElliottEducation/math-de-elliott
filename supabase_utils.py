from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(email: str):
    """ Simulated login: returns user if valid email. """
    if not email or "@" not in email:
        return None
    return {"email": email}

def register_user(email: str):
    """ Simulated register: just return user object """
    if not email or "@" not in email:
        return None
    return {"email": email}
