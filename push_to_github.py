"""
Direct GitHub API Repository Creator & Uploader for YashRajKeshri.
Creates the repository 'Netflix-SQL-Analytics' on GitHub (if not already created)
and uploads/syncs all project files directly via GitHub REST API.
"""

import base64
import os
import sys
from pathlib import Path
import urllib.request
import json

REPO_NAME = "Netflix-SQL-Analytics"
GITHUB_USER = "YashRajKeshri"
BASE_DIR = Path(__file__).resolve().parent

IGNORE_PATTERNS = [
    ".git",
    "venv",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    ".DS_Store",
    "data/netflix_analytics.db",
]


def should_ignore(path: Path) -> bool:
    rel = path.relative_to(BASE_DIR).as_posix()
    for pat in IGNORE_PATTERNS:
        if rel == pat or rel.startswith(pat + "/") or path.name == pat:
            return True
    return False


def collect_files():
    file_list = []
    for root, dirs, files in os.walk(BASE_DIR):
        root_path = Path(root)
        if should_ignore(root_path):
            continue
        for f in files:
            p = root_path / f
            if not should_ignore(p):
                rel = p.relative_to(BASE_DIR).as_posix()
                file_list.append((rel, p))
    return file_list


def create_or_verify_repo(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PortfolioUploader",
    }
    
    # Check if repo exists
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"✅ Repository https://github.com/{GITHUB_USER}/{REPO_NAME} exists.")
                return
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"⚠️ Note on checking repo: {e.code} - {e.reason}")

    # Create repo
    print(f"📦 Creating new public repository '{REPO_NAME}' on GitHub...")
    create_url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": REPO_NAME,
        "description": "End-to-End Netflix Subscriber SQL Analytics, Cohort Engagement & Revenue Optimization Platform in MySQL 8.0+",
        "private": False,
        "auto_init": True,
    }).encode("utf-8")
    
    post_req = urllib.request.Request(create_url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(post_req) as resp:
            if resp.status in [200, 201]:
                print("✅ Repository created successfully on GitHub!")
    except urllib.error.HTTPError as e:
        print(f"⚠️ Note on repo creation: {e.code} - {e.reason}")


def push_with_git(token: str) -> bool:
    try:
        import subprocess
        remote_url = f"https://x-access-token:{token}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        env = os.environ.copy()
        env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        env["GIT_CONFIG_SYSTEM"] = "/dev/null"
        
        # Check if git repo is initialized
        if not (BASE_DIR / ".git").exists():
            subprocess.run(["git", "init"], cwd=BASE_DIR, env=env, check=True)
            subprocess.run(["git", "config", "user.name", GITHUB_USER], cwd=BASE_DIR, env=env, check=True)
            subprocess.run(["git", "config", "user.email", "yashr8181apl@gmail.com"], cwd=BASE_DIR, env=env, check=True)
            subprocess.run(["git", "add", "."], cwd=BASE_DIR, env=env, check=True)
            subprocess.run(["git", "commit", "-m", "feat: initial commit for Netflix-SQL-Analytics"], cwd=BASE_DIR, env=env, check=True)

        print(f"🚀 Pushing git commits to https://github.com/{GITHUB_USER}/{REPO_NAME}...")
        res = subprocess.run(["git", "push", "-u", remote_url, "main", "--force"], cwd=BASE_DIR, env=env, capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ Successfully pushed to GitHub via Git!")
            return True
        else:
            print(f"⚠️ Git push notice: {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"⚠️ Git push error: {e}")
        return False


def upload_via_github_api(token: str):
    create_or_verify_repo(token)

    # Try fast git push first
    if push_with_git(token):
        print(f"\n🎉 Repository successfully live at: https://github.com/{GITHUB_USER}/{REPO_NAME}\n")
        return

    # Fallback to API upload
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PortfolioUploader",
        "Content-Type": "application/json",
    }

    files = collect_files()
    print(f"\n🚀 Uploading {len(files)} project files directly to GitHub main branch via REST API...\n")

    for rel_path, full_path in files:
        try:
            with open(full_path, "rb") as f:
                content_bytes = f.read()

            content_b64 = base64.b64encode(content_bytes).decode("utf-8")

            # Check if file exists on GitHub to get sha
            url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{rel_path}"
            get_req = urllib.request.Request(url, headers=headers, method="GET")
            sha = None
            try:
                with urllib.request.urlopen(get_req) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        sha = data.get("sha")
            except urllib.error.HTTPError:
                pass

            payload_dict = {
                "message": f"feat: add {rel_path}",
                "content": content_b64,
                "branch": "main",
            }
            if sha:
                payload_dict["sha"] = sha

            put_data = json.dumps(payload_dict).encode("utf-8")
            put_req = urllib.request.Request(url, data=put_data, headers=headers, method="PUT")
            with urllib.request.urlopen(put_req) as resp:
                if resp.status in [200, 201]:
                    print(f"  ✓ {rel_path}")
                else:
                    print(f"  ✗ {rel_path} ({resp.status})")
        except Exception as e:
            print(f"  ✗ Error uploading {rel_path}: {str(e)}")

    print(f"\n🎉 All files uploaded successfully!")
    print(f"🌟 View your live repository at: https://github.com/{GITHUB_USER}/{REPO_NAME}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    else:
        token = input("Enter your GitHub Personal Access Token: ").strip()

    if not token:
        print("❌ Error: GitHub Token is required.")
        sys.exit(1)

    upload_via_github_api(token)
