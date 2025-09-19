#!/bin/bash

# Student Setup Helper Script
# This script helps students quickly verify their GitHub template repository setup

echo "🎓 Student Template Repository Setup Checker"
echo "============================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ This doesn't appear to be a git repository"
    echo "   Please run this script in your forked repository directory"
    exit 1
fi

# Get repository information
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "unknown")
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

echo "📁 Repository Info:"
echo "   URL: $REPO_URL"
echo "   Branch: $CURRENT_BRANCH"
echo ""

# Check if it's likely a student's template repository
if [[ $REPO_URL == *"github.com"* ]] && [[ $REPO_URL != *"ESIEE-Python"* ]]; then
    echo "✅ This appears to be a student's repository (not in ESIEE-Python org)"
    echo "   Good! You should work in your own repository created from template"
elif [[ $REPO_URL == *"ESIEE-Python"* ]]; then
    echo "⚠️  This appears to be the template repository (ESIEE-Python org)"
    echo "   Students should create their own repository using 'Use this template'"
    echo "   Steps:"
    echo "   1. Go to the ESIEE-Python template repository"
    echo "   2. Click 'Use this template' (green button)"
    echo "   3. Create repository in your personal account"
    echo "   4. Clone YOUR repository, not the template"
else
    echo "❓ Repository origin unclear"
fi
echo ""

# Check for required files
echo "📋 Checking required files:"
files_to_check=(
    "run_supabase_test.sh"
    "check_secrets.py"
    "test_supabase_permissions.py"
    "04-primes/.python/update_sb.py"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done
echo ""

# Check Python environment
echo "🐍 Python Environment Check:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found"
fi

if [ -f "requirements.txt" ]; then
    echo "   📦 requirements.txt found"
elif [ -f ".venv/pyvenv.cfg" ]; then
    echo "   📦 Virtual environment detected"
else
    echo "   ⚠️  No requirements.txt or venv detected"
fi
echo ""

# Run the secrets check
echo "🔐 Checking Secrets Configuration:"
if [ -f "check_secrets.py" ]; then
    python3 check_secrets.py
else
    echo "❌ check_secrets.py not found - cannot verify secrets"
fi

echo ""
echo "📚 Next Steps:"
echo "1. If secrets are missing, see SECRETS_SETUP_GUIDE.md"
echo "2. To test Supabase connection: ./run_supabase_test.sh"
echo "3. For help, contact your instructor or TA"
echo ""
echo "🎯 Quick Commands:"
echo "   Test connection: ./run_supabase_test.sh"
echo "   Check schema:    python3 check_schema.py"
echo "   View setup guide: cat SECRETS_SETUP_GUIDE.md"