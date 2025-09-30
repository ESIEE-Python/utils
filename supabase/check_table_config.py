#!/usr/bin/env python3
"""
Script to check Supabase table configuration and RLS policies
"""
import os
import json
import requests


def check_table_config():
    """Check table schema and RLS configuration"""
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_table = os.environ.get('SUPABASE_TABLE', 'marks')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        return
    
    print(f"🔍 Checking configuration for table: {supabase_table}")
    print("=" * 50)
    
    # Check if table exists and get schema
    print("\n📋 Table Schema:")
    try:
        # This endpoint gives us table information
        response = requests.get(
            f"{supabase_url}/rest/v1/{supabase_table}",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Range": "0-0"  # Just get headers, no data
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Table exists and is accessible")
            
            # Try to get one record to see the structure
            response_data = requests.get(
                f"{supabase_url}/rest/v1/{supabase_table}?select=*&limit=1",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}"
                },
                timeout=10
            )
            
            if response_data.status_code == 200:
                data = response_data.json()
                if data:
                    print("   📊 Sample record structure:")
                    for key in data[0].keys():
                        print(f"      - {key}")
                else:
                    print("   📊 Table is empty")
        
        elif response.status_code == 401:
            print("   ❌ Authentication failed")
        elif response.status_code == 403:
            print("   ❌ Access forbidden - might be RLS issue")
        elif response.status_code == 404:
            print("   ❌ Table not found")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error checking table: {e}")
    
    # Check RLS status (this requires specific endpoint)
    print(f"\n🔒 Row Level Security (RLS) Check:")
    print("   💡 To check RLS status, you can:")
    print("   1. Go to your Supabase dashboard")
    print("   2. Navigate to Database > Tables")
    print(f"   3. Find the '{supabase_table}' table")
    print("   4. Check if 'RLS enabled' is toggled on")
    print("")
    print("   If RLS is enabled:")
    print("   - anon key: Subject to RLS policies")
    print("   - service_role key: Bypasses RLS (full access)")
    
    # Provide troubleshooting guide
    print(f"\n🛠️  Troubleshooting Guide:")
    print("   For FORKED repositories:")
    print("")
    print("   1. Environment Variables:")
    print("      - Ensure GitHub secrets are properly set in the fork")
    print("      - SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE")
    print("")
    print("   2. Key Type:")
    print("      - Use service_role key for full access")
    print("      - anon key requires proper RLS policies")
    print("")
    print("   3. RLS Policies (if using anon key):")
    print("      - Create INSERT policy allowing the operation")
    print("      - Example policy: 'Allow authenticated users to insert'")
    print("")
    print("   4. Table Permissions:")
    print("      - Ensure the table allows INSERT operations")
    print("      - Check column constraints and requirements")


if __name__ == "__main__":
    check_table_config()