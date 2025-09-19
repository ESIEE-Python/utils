#!/bin/bash
# Test script runner with environment setup
# 
# Usage: 
# 1. Set your environment variables:
#    export SUPABASE_URL="your_supabase_url"
#    export SUPABASE_KEY="your_supabase_key" 
#    export SUPABASE_TABLE="marks"  # or your table name
# 
# 2. Run this script:
#    ./run_supabase_test.sh

echo "🧪 Supabase Permissions Test Runner"
echo "=================================="

# Check if environment variables are set
if [ -z "$SUPABASE_URL" ]; then
    echo "❌ SUPABASE_URL not set. Please export it first:"
    echo "   export SUPABASE_URL='https://your-project.supabase.co'"
    exit 1
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "❌ SUPABASE_KEY not set. Please export it first:"
    echo "   export SUPABASE_KEY='your_key_here'"
    exit 1
fi

if [ -z "$SUPABASE_TABLE" ]; then
    echo "⚠️  SUPABASE_TABLE not set, using default 'marks'"
    export SUPABASE_TABLE="marks"
fi

echo "Running test with:"
echo "  URL: $SUPABASE_URL"
echo "  Table: $SUPABASE_TABLE"
echo "  Key: ${SUPABASE_KEY:0:20}..."
echo ""

# Run the Python test script
/home/daniel-courivaud/Desktop/Python-github-ci/.venv/bin/python /home/daniel-courivaud/Desktop/Python-github-ci/test_supabase_permissions.py