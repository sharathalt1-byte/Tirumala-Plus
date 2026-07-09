from supabase import create_client

from tirumala_pulse.config.settings import (
    SUPABASE_URL,
    SUPABASE_KEY
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)