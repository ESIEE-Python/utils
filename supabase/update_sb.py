import os
import sys
import json
import requests


def main(pytest_score, pytest_string, pylint_score):
    print("start updating db")

    github_sha = os.environ['GITHUB_SHA']
    github_run_number = os.environ['GITHUB_RUN_NUMBER']
    github_actor = os.environ['GITHUB_ACTOR']
    github_repository = os.environ['GITHUB_REPOSITORY']

    supabase_url = os.environ['SUPABASE_URL']
    supabase_key = os.environ['SUPABASE_KEY']
    supabase_table = os.environ.get('SUPABASE_TABLE', 'marks')  # default to 'ci_data'

    print(f"{github_sha=}")
    print(f"{github_run_number=}")
    print(f"{github_actor=}")
    print(f"{github_repository=}")

    data = {
        'actor': github_actor,
        'pytest_score': pytest_score,
        'pytest_string': pytest_string,
        'pylint_score': pylint_score,
        'sha': github_sha,
        'run_number': github_run_number,
        'repo': github_repository,
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
            data=json.dumps(data)
        )
        response.raise_for_status()
        print("Record inserted:", response.json())
    except Exception as e:
        print("Error inserting record:", e)
        sys.exit(1)

    print("end updating db")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_sb.py pytest_score pytest_string pylint_score")
        sys.exit(1)

    main(float(sys.argv[1]), sys.argv[2], float(sys.argv[3]))