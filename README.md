# Manage GitHub exercises repos






## Supabase Integration for CI Results

This folder contains scripts and documentation for sending CI results to a Supabase database.

### Table Schema

The `marks` table should have the following columns:
- `id` (bigint, primary key, auto-increment)
- `created_at` (timestamp with time zone, default: now())
- `actor` (text)
- `pylint_score` (real/float)
- `pytest_score` (real/float)
- `pytest_string` (text)
- `sha` (varchar)
- `run_number` (smallint)
- `repo` (text)

### Usage

1. Set your Supabase credentials in the scripts or as environment variables:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase service role key
   - `SUPABASE_TABLE`: Table name (default: `marks`)

2. Run the test script to insert a record:
   ```bash
   python test_supabase.py
   ```

### Security
- Always use the **service role key** for inserts.
- Never share your service role key publicly.

### Troubleshooting
- 401 Unauthorized: Check your key and project URL.
- 400 Bad Request: Ensure your payload matches the table schema exactly.
