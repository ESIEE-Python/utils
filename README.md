# Manage GitHub exercises repos

## Supabase Integration for CI Results

This folder contains scripts and documentation for sending CI results to a Supabase database, including comprehensive diagnostic tools for testing permissions and troubleshooting issues.

### Files Overview

#### Core Scripts
- `04-primes/.python/update_sb.py` - Main script for updating Supabase from CI/CD
- `test_supabase.py` - Basic Supabase connection test

#### Diagnostic & Testing Tools
- `test_supabase_permissions.py` - Comprehensive permissions and write access test
- `run_supabase_test.sh` - Easy test runner with environment setup
- `check_schema.py` - Table schema inspector and data type checker
- `check_table_config.py` - RLS and configuration troubleshooting guide
- `check_secrets.py` - Verify GitHub secrets configuration
- `student_setup_check.sh` - All-in-one setup verification for students

#### Documentation
- `STUDENT_TEMPLATE_INSTRUCTIONS.md` - Quick setup guide for students
- `SECRETS_SETUP_GUIDE.md` - Comprehensive setup and troubleshooting guide

### Table Schema

The `marks` table should have the following columns:
- `id` (bigint, primary key, auto-increment) ⚠️ REQUIRED
- `created_at` (timestamp with time zone, default: now()) ⚠️ REQUIRED
- `actor` (text) - GitHub username
- `pylint_score` (real/float) - Pylint score
- `pytest_score` (real/float) - Pytest score
- `pytest_string` (text) - Pytest output summary
- `sha` (varchar) - Git commit SHA
- `run_number` (smallint) - GitHub Actions run number (must be integer!)
- `repo` (text) - Repository name

### Quick Setup & Testing

#### 1. Environment Setup
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your_service_role_key_here"
export SUPABASE_TABLE="marks"  # optional, defaults to 'marks'
```

#### 2. Run Comprehensive Test
```bash
# Make script executable (first time only)
chmod +x run_supabase_test.sh

# Run the full diagnostic test
./run_supabase_test.sh
```

This will test:
- ✅ Key type analysis (service_role vs anon)
- ✅ Basic connection
- ✅ Read permissions
- ✅ Write permissions with proper data types
- ✅ Error diagnosis and solutions

#### 3. Check Table Schema
```bash
python check_schema.py
```

### For Template-Based Student Repositories

**✅ Your setup WILL work for student template repositories if:**
1. Using **service_role key** (recommended for full access)
2. Students create repository from template (not fork)
3. GitHub secrets properly configured in student's repository:
   - `SUPABASE_URL`
   - `SUPABASE_KEY` 
   - `SUPABASE_TABLE` (optional)

**⚠️ Common Issues:**
- Students fork instead of using template
- Students work in template repo instead of their own
- Wrong data types (especially `run_number` must be integer)
- Secrets not configured in student's repository

**📚 Student Instructions:** See `STUDENT_TEMPLATE_INSTRUCTIONS.md`

### Usage

1. **From CI/CD (GitHub Actions):**
   ```python
   # This is handled automatically by update_sb.py
   # Environment variables are set via GitHub secrets
   ```

2. **Manual Testing:**
   ```bash
   # Use the comprehensive test runner
   ./run_supabase_test.sh
   
   # Or run individual diagnostic scripts
   python test_supabase_permissions.py
   python check_schema.py
   python check_table_config.py
   ```

### Security
- ✅ **Use service role key** for CI/CD (bypasses RLS, full access)
- ✅ Store keys in GitHub secrets, never in code
- ✅ Service role key format: `eyJ...` (long JWT token)
- ❌ Don't use anon key unless you have proper RLS policies

### Troubleshooting Guide

#### Quick Diagnosis
Run the diagnostic test to get instant feedback:
```bash
./run_supabase_test.sh
```

#### Common Error Solutions

**🔑 Authentication Errors:**
- `401 Unauthorized` → Check SUPABASE_KEY and SUPABASE_URL
- `403 Forbidden` → RLS blocking access (use service_role key)

**📊 Data Type Errors:**
- `invalid input syntax for type smallint` → `run_number` must be integer
- `22P02 error` → Check data types match table schema exactly

**🗄️ Table Errors:**
- `404 Not Found` → Check SUPABASE_TABLE name
- `relation does not exist` → Table doesn't exist in database

**🔐 Forked Repository Issues:**
- Missing secrets → Configure GitHub secrets in fork settings
- Permission denied → Ensure service_role key is used
- Wrong environment → Verify SUPABASE_URL points to correct project

#### Advanced Debugging
1. **Check key type:** `python test_supabase_permissions.py`
2. **Inspect schema:** `python check_schema.py` 
3. **Verify config:** `python check_table_config.py`

### Data Types Reference
```python
# Correct data format for update_sb.py
{
    'actor': 'string',           # GitHub username
    'pytest_score': float,       # 0.0 - 100.0
    'pytest_string': 'string',   # Test output summary
    'pylint_score': float,       # 0.0 - 10.0
    'sha': 'string',            # Git commit SHA
    'run_number': int,          # GitHub run number (INTEGER!)
    'repo': 'string'            # owner/repo format
}
```
