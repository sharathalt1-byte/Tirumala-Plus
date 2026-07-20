import os

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# WordPress REST API endpoint
TTD_NEWS_BASE_URL = os.getenv(
    "TTD_NEWS_BASE_URL",
    "https://news.tirumala.org/wp-json/wp/v2/posts",
)

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing")