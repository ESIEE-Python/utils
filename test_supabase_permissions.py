#!/usr/bin/env python3
"""
Test script to verify Supabase key type and write permissions
"""
import os
import json
import requests
import base64
from datetime import datetime


def decode_jwt_payload(token):
    """Decode JWT payload to understand key type"""
    try:
        # Split the token and get the payload part
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Add padding if needed
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        
        # Decode base64
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        print(f"Error decoding JWT: {e}")
        return None


def test_supabase_connection():
    """Test Supabase connection and key permissions"""
    
    # Get environment variables
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_table = os.environ.get('SUPABASE_TABLE', 'marks')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        return False
    
    print(f"🔗 Supabase URL: {supabase_url}")
    print(f"📋 Table: {supabase_table}")
    print(f"🔑 Key (first 20 chars): {supabase_key[:20]}...")
    
    # Analyze the key type
    print("\n🔍 Analyzing key type...")
    payload = decode_jwt_payload(supabase_key)
    
    if payload:
        role = payload.get('role', 'unknown')
        iss = payload.get('iss', 'unknown')
        print(f"   Role: {role}")
        print(f"   Issuer: {iss}")
        
        if role == 'service_role':
            print("   ✅ Service role key detected - should have full access")
        elif role == 'anon':
            print("   ⚠️  Anonymous key detected - subject to RLS policies")
        else:
            print(f"   ❓ Unknown role: {role}")
    else:
        print("   ❌ Could not decode key - might not be a valid JWT")
    
    # Test basic connection
    print("\n🔌 Testing basic connection...")
    try:
        response = requests.get(
            f"{supabase_url}/rest/v1/",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}"
            },
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Basic connection successful")
        else:
            print(f"   ❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    # Test table read access
    print(f"\n📖 Testing read access to '{supabase_table}' table...")
    try:
        response = requests.get(
            f"{supabase_url}/rest/v1/{supabase_table}?select=*&limit=1",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}"
            },
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Read access successful")
            data = response.json()
            print(f"   📊 Retrieved {len(data)} record(s)")
        else:
            print(f"   ❌ Read access failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Read test error: {e}")
        return False
    
    # Test write access with a dummy record
    print(f"\n✍️  Testing write access to '{supabase_table}' table...")
    test_data = {
        'actor': 'test_user',
        'pytest_score': 99.9,
        'pytest_string': 'TEST_RUN',
        'pylint_score': 10.0,
        'sha': 'test_sha_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
        'run_number': 999,  # Use integer instead of string
        'repo': 'test/repo',
    }
    
    try:
        response = requests.post(
            f"{supabase_url}/rest/v1/{supabase_table}",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            data=json.dumps(test_data),
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("   ✅ Write access successful!")
            print(f"   📝 Test record created: {response.json()}")
            return True
        else:
            print(f"   ❌ Write access failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
            # Common error interpretations
            if response.status_code == 401:
                print("   💡 Suggestion: Authentication failed - check your SUPABASE_KEY")
            elif response.status_code == 403:
                print("   💡 Suggestion: Insufficient permissions - RLS policy might be blocking writes")
            elif response.status_code == 404:
                print("   💡 Suggestion: Table not found - check SUPABASE_TABLE name")
            elif response.status_code == 422:
                print("   💡 Suggestion: Data validation error - check table schema")
            
            return False
            
    except Exception as e:
        print(f"   ❌ Write test error: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Supabase Permissions Test")
    print("=" * 40)
    
    success = test_supabase_connection()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed! Your setup should work for forked repos.")
    else:
        print("🚨 Some tests failed. Check the issues above.")
        print("\n💡 Common solutions:")
        print("   - Ensure SUPABASE_KEY is a service_role key for full access")
        print("   - Check RLS policies on your table")
        print("   - Verify environment variables are properly set in GitHub secrets")