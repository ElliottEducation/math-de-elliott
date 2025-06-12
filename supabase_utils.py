from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(email: str, password: str = "defaultPassword123") -> dict:
    """
    Register user using Supabase Auth. Returns user dict if successful.
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response.user
    except Exception as e:
        print("Registration error:", e)
        return None

def login_user(email: str, password: str = "defaultPassword123") -> dict:
    """
    Login user using Supabase Auth. Returns session dict if successful.
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user
    except Exception as e:
        print("Login error:", e)
        return None
