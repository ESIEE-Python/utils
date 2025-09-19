# GitHub Secrets Setup Guide for Template-Based Repositories

## 🎯 Overview
When students create repositories from your GitHub organization template, they need to configure their own secrets since **template-based repositories are independent and don't inherit secrets from the template**.

## 🏫 For Students: Setting Up Secrets in Your Template Repository

### Step 1: Create Repository from Template
1. Go to the template repository in the ESIEE-Python organization
2. Click **"Use this template"** button (green button, top right)
3. Choose **"Create a new repository"**
4. Select your personal GitHub account as owner
5. Name your repository (follow instructor guidelines)
6. Set visibility (usually Public for coursework)
7. Click **"Create repository from template"**

### Step 2: Configure Secrets
1. Go to **your new repository** on GitHub (now in your account)
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** button

### Step 3: Add Required Secrets
Add these three secrets one by one:

#### Secret 1: SUPABASE_URL
- **Name:** `SUPABASE_URL`
- **Value:** `https://your-project.supabase.co` (provided by instructor)

#### Secret 2: SUPABASE_KEY  
- **Name:** `SUPABASE_KEY`
- **Value:** `eyJ...` (service role key provided by instructor)

#### Secret 3: SUPABASE_TABLE
- **Name:** `SUPABASE_TABLE`
- **Value:** `marks` (or table name specified by instructor)

### Step 4: Test Your Setup
```bash
# Clone your new repository and test
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

# Check if secrets work (in GitHub Actions)
# Push a commit to trigger the workflow

# Test locally (if you have the values)
export SUPABASE_URL="your_url_here"
export SUPABASE_KEY="your_key_here"  
export SUPABASE_TABLE="marks"
./run_supabase_test.sh
```

## 👨‍🏫 For Instructors: Managing Template-Based Student Repositories

### ✅ Advantages of Template Approach
- **Independent repositories:** Students have full control
- **No fork limitations:** All GitHub features available
- **Cleaner workflow:** No upstream/downstream confusion
- **Better for submissions:** Each student has their own repo
- **No pull request complexity:** Direct commits to main branch

### Option 1: Manual Secret Distribution (Recommended)
**Pros:** Simple, secure, works well with templates
**Cons:** Manual setup for each student

1. **Create template repository** with all scripts and documentation
2. **Provide secrets via secure channel** (LMS, email, etc.)
3. **Students use template** to create their repository
4. **Students follow setup guide** to configure secrets
5. **Use diagnostic scripts** for verification

### Option 2: Template with Secrets Documentation
**Pros:** Self-service, scales well
**Cons:** Requires clear documentation

1. **Include setup scripts** in template (already done!)
2. **Create clear README** with secret requirements
3. **Provide secrets via LMS/course portal**
4. **Students self-configure** using provided tools

### Option 3: Automated Secret Setup (Advanced)
**Pros:** Minimal manual work
**Cons:** Complex initial setup

```bash
# Example: Setup script students run after template creation
curl -s https://course-server.edu/setup-secrets.sh | bash
# Script prompts for course code, then configures secrets
```

### Option 4: GitHub Classroom Integration
**Pros:** Automated repository creation and management
**Cons:** Requires GitHub Classroom setup

- Use GitHub Classroom assignments
- Template repositories automatically created for students
- Secrets can be pre-configured per assignment
- Automatic grading integration possible

## 🔍 Checking Secrets Configuration

### For Students: Check Your Setup
```bash
# Run the secret checker
python check_secrets.py

# Run full Supabase test
./run_supabase_test.sh
```

### For Instructors: Verify Student Setup
1. **Ask students to run:** `python check_secrets.py`
2. **Check GitHub Actions logs** in student template repositories
3. **Monitor Supabase database** for test entries
4. **Use diagnostic scripts** to troubleshoot issues

## 🚨 Common Issues & Solutions

### Issue: "Template doesn't include latest scripts"
**Solution:** Update template repository, ask students to re-download files

### Issue: "SUPABASE_KEY unauthorized" 
**Solution:** 
- Check if key is service_role (not anon)
- Verify key wasn't truncated when copying
- Ensure URL matches the key's project

### Issue: "Student created fork instead of using template"
**Solution:** 
- Clarify instructions: "Use this template" vs "Fork"
- Template creates independent repo, fork creates linked repo
- Students need independent repos for this workflow

### Issue: "Repository not in student's account"
**Solution:**
- Ensure student selected their personal account as owner
- Check repository URL shows student username, not ESIEE-Python

### Issue: "Table not found"
**Solution:**
- Check SUPABASE_TABLE name spelling
- Verify table exists in the database
- Ensure key has access to the table

### Issue: "Data type errors"
**Solution:**
- Use the schema checker: `python check_schema.py`
- Verify `run_number` is integer, not string
- Check all data types match table schema

## 📋 Checklist for Instructors

- [ ] **Prepare secrets** (URL, service role key, table name)
- [ ] **Test with a fork** yourself first
- [ ] **Create clear instructions** for students
- [ ] **Set up monitoring** (database, error tracking)
- [ ] **Plan troubleshooting** (office hours, TA support)
- [ ] **Verify security** (key permissions, RLS if needed)

## 🔐 Security Considerations

### Service Role Key Sharing
- **Risk:** Full database access for all students
- **Mitigation:** 
  - Use RLS policies to limit access
  - Monitor database activity
  - Rotate keys if compromised
  - Consider per-student keys for high-security needs

### Alternative: Row Level Security (RLS)
```sql
-- Example RLS policy for student access
CREATE POLICY "Students can insert their own records" ON marks
FOR INSERT WITH CHECK (actor = current_setting('request.jwt.claims', true)::json->>'sub');
```

## 📞 Support Resources

- **Diagnostic Scripts:** `check_secrets.py`, `run_supabase_test.sh`
- **Schema Checker:** `check_schema.py`
- **Documentation:** This guide + README.md
- **GitHub Docs:** [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/encrypted-secrets)