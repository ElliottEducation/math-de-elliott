from supabase import create_client
import os
from dotenv import load_dotenv

# Load .env configuration
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_user(email: str):
    """
    Simulate a login. You can later replace this with real Supabase auth logic.
    """
    if not email or "@" not in email:
        return None
    return {"email": email}
