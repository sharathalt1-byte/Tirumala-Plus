import os
from pathlib import Path

from dotenv import load_dotenv

# Find the project root (tirumala-pulse)
BASE_DIR = Path(__file__).resolve().parents[3]

# Explicitly load .env from the project root
load_dotenv(BASE_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_PUBLISHABLE_KEY is missing")