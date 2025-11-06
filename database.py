# database.py
import os
from supabase import create_client, Client

#oad_dotenv()

#DATABASE_URL = os.getenv("SUPABASE_DB_URL")

url: str = "https://hsvsfztqkrnvnovxxkfq.supabase.co"
#url: str = "db.hsvsfztqkrnvnovxxkfq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhzdnNmenRxa3Judm5vdnh4a2ZxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjM2MDI4NCwiZXhwIjoyMDc3OTM2Mjg0fQ.550efXrSZVLGkfVHi9I0nb9L7UBbSsycSNlfoC-cNjw"
supabase: Client = create_client(url, key)