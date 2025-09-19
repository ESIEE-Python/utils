# 🎓 Student Instructions: Using the Template Repository

## 📝 Quick Setup Guide for Students

### Step 1: Create Your Repository from Template
1. **Go to the ESIEE-Python template repository** (the one your instructor shared)
2. **Click the green "Use this template" button** (top right, next to Code button)
3. **Select "Create a new repository"**
4. **Fill out the form:**
   - Owner: Select **your personal GitHub account** (not ESIEE-Python)
   - Repository name: Follow your instructor's naming convention
   - Description: Optional
   - Visibility: **Public** (usually required for coursework)
5. **Click "Create repository from template"**

### Step 2: Clone YOUR Repository
```bash
# Clone YOUR repository (not the template)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Step 3: Configure Secrets
1. **Go to YOUR repository** on GitHub (should show your username in URL)
2. **Settings** → **Secrets and variables** → **Actions**
3. **Add these three secrets** (get values from instructor):

#### Required Secrets:
- **Name:** `SUPABASE_URL` **Value:** `https://your-project.supabase.co`
- **Name:** `SUPABASE_KEY` **Value:** `eyJ...` (long key from instructor)  
- **Name:** `SUPABASE_TABLE` **Value:** `marks`

### Step 4: Test Your Setup
```bash
# Run the setup checker
./student_setup_check.sh

# Test Supabase connection
./run_supabase_test.sh
```

## ✅ Success Indicators
- ✅ Repository URL shows **your username**, not ESIEE-Python
- ✅ You can push commits to your repository
- ✅ `./run_supabase_test.sh` shows "All tests passed!"
- ✅ GitHub Actions run successfully after pushing code

## 🚨 Common Mistakes to Avoid

### ❌ Wrong: Forking Instead of Using Template
- **Don't click "Fork"** - this creates a linked copy
- **Do click "Use this template"** - this creates an independent copy

### ❌ Wrong: Working in Template Repository
- Don't clone: `git clone https://github.com/ESIEE-Python/...`
- Do clone: `git clone https://github.com/YOUR_USERNAME/...`

### ❌ Wrong: Missing Secrets
- Secrets must be set in **your repository**, not the template
- Template repositories don't have access to instructor's secrets

## 🆘 Getting Help

### Self-Diagnosis
```bash
# Check if you're in the right repository
./student_setup_check.sh

# Test your secrets configuration  
python check_secrets.py

# Verify Supabase connection
./run_supabase_test.sh
```

### If You Need Help
1. **Run diagnostic scripts** and share the output
2. **Check repository URL** - should be `github.com/YOUR_USERNAME/...`
3. **Verify secrets are set** in your repository settings
4. **Contact instructor/TA** with specific error messages

## 🎯 Quick Reference Commands

```bash
# Initial setup check
./student_setup_check.sh

# Test Supabase connection
./run_supabase_test.sh

# Check secrets configuration
python check_secrets.py

# View detailed setup guide
cat SECRETS_SETUP_GUIDE.md

# Check table schema
python check_schema.py
```

---
💡 **Remember:** You're working with YOUR OWN repository created from the template, not the original template repository!