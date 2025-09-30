#!/bin/bash

# Student Setup Helper Script
# This script helps students quickly verify their GitHub template repository setup

echo "🎓 Student Template Repository Setup Checker"
echo "============================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ This doesn't appear to be a git repository"
    echo "   Please run this script in your repository directory"
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
    echo "✅ This appears to be a student's repository"
elif [[ $REPO_URL == *"ESIEE-Python"* ]]; then
    echo "⚠️  This appears to be the template repository (ESIEE-Python org)"
    echo "   Students should create their own repository using 'Use this template'"
    echo "   Steps:"
    echo "   1. Go to the ESIEE-Python template repository"
    echo "   2. Click 'Use this template' (green button)"
    echo "   3. Create repository in your personal account"
else
    echo "❓ Repository origin unclear"
fi
echo ""

# Check Python environment
echo "🐍 Python Environment Check:"
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python 3 not found"
fi

