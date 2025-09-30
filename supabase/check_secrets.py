#!/usr/bin/env python3
"""
Script to check if GitHub secrets are properly configured
This helps students verify their forked repository setup
"""
import os
import sys


def check_required_secrets():
    """Check if all required environment variables/secrets are set"""
    
    print("🔐 GitHub Secrets Configuration Check")
    print("=" * 45)
    
    required_secrets = {
        'SUPABASE_URL': 'Your Supabase project URL',
        'SUPABASE_KEY': 'Your Supabase service role key', 
        'SUPABASE_TABLE': 'Table name (optional, defaults to "marks")'
    }
    
    github_vars = {
        'GITHUB_ACTOR': 'GitHub username (automatically set)',
        'GITHUB_REPOSITORY': 'Repository name (automatically set)',
        'GITHUB_SHA': 'Commit SHA (automatically set)',
        'GITHUB_RUN_NUMBER': 'Run number (automatically set)'
    }
    
    all_good = True
    
    print("📋 Required Secrets (must be set manually):")
    for var, description in required_secrets.items():
        value = os.environ.get(var)
        if value:
            if var == 'SUPABASE_KEY':
                display_value = value[:20] + "..." if len(value) > 20 else value
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: NOT SET")
            print(f"      → {description}")
            all_good = False
            if var != 'SUPABASE_TABLE':  # This one is optional
                all_good = False
    
    print(f"\n🤖 GitHub Environment Variables (automatic):")
    for var, description in github_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚠️  {var}: Not set (normal in local environment)")
            print(f"      → {description}")
    
    print(f"\n" + "=" * 45)
    
    if all_good:
        print("🎉 All required secrets are configured!")
        return True
    else:
        print("❌ Some secrets are missing. See setup guide below.")
        print_setup_guide()
        return False


def print_setup_guide():
    """Print detailed setup instructions"""
    
    print(f"\n📚 SETUP GUIDE FOR FORKED REPOSITORIES")
    print("=" * 50)
    
    print("🏫 FOR STUDENTS:")
    print("1. Create repository from template (ESIEE-Python organization)")
    print("2. Go to your new repository on GitHub (in your account)")
    print("3. Click: Settings → Secrets and variables → Actions")
    print("4. Click 'New repository secret' for each required secret:")
    print()
    print("   Secret Name: SUPABASE_URL")
    print("   Secret Value: https://your-project.supabase.co")
    print()
    print("   Secret Name: SUPABASE_KEY") 
    print("   Secret Value: eyJ... (your service role key)")
    print()
    print("   Secret Name: SUPABASE_TABLE")
    print("   Secret Value: marks")
    print()
    
    print("👨‍🏫 FOR INSTRUCTORS:")
    print("• Provide students with:")
    print("  - SUPABASE_URL (same for all students)")
    print("  - SUPABASE_KEY (service role key - same for all)")
    print("  - SUPABASE_TABLE (usually 'marks')")
    print("• Create template repository with all diagnostic scripts")
    print("• Students create their own repo from template")
    print("• Test with a student template repository yourself first")
    print()
    
    print("🔒 SECURITY NOTES:")
    print("• Service role key has full database access")
    print("• Only share with trusted students")
    print("• Consider using RLS policies for additional security")
    print("• Monitor database access if needed")
    print()
    
    print("🧪 TESTING:")
    print("After setting secrets, students can test with:")
    print("  ./run_supabase_test.sh")


def check_if_in_github_actions():
    """Check if we're running in GitHub Actions environment"""
    
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("🤖 Running in GitHub Actions environment")
        return True
    else:
        print("💻 Running in local environment")
        print("   (GitHub environment variables won't be available)")
        return False


if __name__ == "__main__":
    print("Environment:", "GitHub Actions" if check_if_in_github_actions() else "Local")
    print()
    
    success = check_required_secrets()
    
    if not success:
        sys.exit(1)
    else:
        print("\n✅ Ready to proceed with Supabase operations!")