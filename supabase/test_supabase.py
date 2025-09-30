import os
import json
import requests

# Set your Supabase credentials here or use environment variables
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://antsdkjhthaihqhvnvfw.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'your_service_role_key_here')
SUPABASE_TABLE = os.environ.get('SUPABASE_TABLE', 'marks')                           


# INSTRUCTIONS:
# 1. Get your Supabase URL and keys from: https://app.supabase.com/project/YOUR_PROJECT/settings/api
# 2. Replace the placeholder values above
# 3. NEVER commit real keys to git - use environment variables instead
#




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
