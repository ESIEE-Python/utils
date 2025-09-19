import os
import json
import requests

# Set your Supabase credentials here or use environment variables
SUPABASE_URL = 'https://antsdkjhthaihqhvnvfw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFudHNka2podGhhaWhxaHZudmZ3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDY3NzUzNCwiZXhwIjoyMDY2MjUzNTM0fQ.t2KOyVtkmjgFrCX4pVQQnJSydZG5APAQB2L4ddzbVSk'             # <-- Replace with your Supabase service role key
SUPABASE_TABLE = 'marks'                           # <-- Replace with your table name


# zvX49KM7NiHWBia8A9Fs

# SUPABASE_URL = https://antsdkjhthaihqhvnvfw.supabase.co

# SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFudHNka2podGhhaWhxaHZudmZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2Nzc1MzQsImV4cCI6MjA2NjI1MzUzNH0.tgO2bAz3jaqgALB6vC6uX3vtt49L7D6HyJTvkndFVQo

# SUPABASE_SERVICE_ROLE = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFudHNka2podGhhaWhxaHZudmZ3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDY3NzUzNCwiZXhwIjoyMDY2MjUzNTM0fQ.t2KOyVtkmjgFrCX4pVQQnJSydZG5APAQB2L4ddzbVSk

# SUPABASE_TABLE = "marks"





# Dummy test data
payload = {
    'actor': 'localtest',
    'pylint_score': 9.5,
    'pytest_score': 10.0,
    'pytest_string': 'All tests passed',
    'sha': 'testsha',
    'run_number': 1,
    'repo': 'local/repo',
}

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
}

try:
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=headers,
        data=json.dumps(payload)
    )
    response.raise_for_status()
    print('Record inserted:', response.json())
except Exception as e:
    print('Error inserting record:', e)
