#!/usr/bin/env python3
"""
Script to check the exact table schema and data types
"""
import os
import json
import requests


def get_table_schema():
    """Get the actual table schema from Supabase"""
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_table = os.environ.get('SUPABASE_TABLE', 'marks')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        return
    
    print(f"📋 Table Schema for: {supabase_table}")
    print("=" * 50)
    
    # Try to get schema information using OpenAPI endpoint
    try:
        response = requests.get(
            f"{supabase_url}/rest/v1/",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Accept": "application/openapi+json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            schema = response.json()
            
            # Look for our table in the schema
            if 'definitions' in schema:
                table_def = schema['definitions'].get(supabase_table)
                if table_def and 'properties' in table_def:
                    print("📊 Column definitions:")
                    for column, definition in table_def['properties'].items():
                        col_type = definition.get('type', 'unknown')
                        col_format = definition.get('format', '')
                        required = column in table_def.get('required', [])
                        
                        type_info = col_type
                        if col_format:
                            type_info += f" ({col_format})"
                        
                        required_marker = " ⚠️ REQUIRED" if required else ""
                        print(f"   • {column}: {type_info}{required_marker}")
                else:
                    print(f"❌ Table '{supabase_table}' not found in schema")
            else:
                print("❌ No schema definitions found")
                
        else:
            print(f"❌ Failed to get schema: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error getting schema: {e}")
    
    # Alternative: try to get column info by examining an existing record
    print(f"\n🔍 Attempting to infer schema from existing data...")
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
            data = response.json()
            if data:
                print("📊 Sample data types (inferred):")
                sample = data[0]
                for key, value in sample.items():
                    value_type = type(value).__name__
                    print(f"   • {key}: {value_type} (example: {value})")
            else:
                print("📊 Table is empty - cannot infer types")
        else:
            print(f"❌ Cannot read table data: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error reading sample data: {e}")
    
    print(f"\n💡 Expected data format for your update script:")
    print("   {")
    print("     'actor': 'string',")
    print("     'pytest_score': float,")
    print("     'pytest_string': 'string',")
    print("     'pylint_score': float,")
    print("     'sha': 'string',")
    print("     'run_number': integer,  # ← This was the issue!")
    print("     'repo': 'string'")
    print("   }")


if __name__ == "__main__":
    get_table_schema()