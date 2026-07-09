import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")

# ==========================================================
# Supabase Configuration
# ==========================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_PUBLISHABLE_KEY is missing")

# ==========================================================
# TTD News Configuration
# ==========================================================

TTD_NEWS_BASE_URL = "https://news.tirumala.org"

VERIFY_SSL = False   # Development only