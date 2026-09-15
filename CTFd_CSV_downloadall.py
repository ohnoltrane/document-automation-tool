import os
import re
import urllib.parse
import requests

# To download all Export CSVs on CTFd only

# --- CONFIGURATION ---
CTFD_URL = "https://<event_name>.ctfd.io"
# Use your actual CTFd admin username and password
USERNAME = "<user>"
PASSWORD = "<password>"
OUTPUT_DIR = "./ctfd_csv_exports"
# ---------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
session = requests.Session()

print("1. Fetching login page...")
login_page = session.get(f"{CTFD_URL}/login")

# Extract CSRF nonce token
nonce_match = re.search(r'name="nonce" type="hidden" value="([^"]+)"', login_page.text)
if not nonce_match:
    nonce_match = re.search(r"csrfNonce': \"([^\"]+)\"", login_page.text)

nonce = nonce_match.group(1) if nonce_match else ""

print("2. Logging into CTFd...")
login_data = {
    "name": USERNAME,
    "password": PASSWORD,
    "nonce": nonce,
    "_submit": "Submit"
}
login_res = session.post(f"{CTFD_URL}/login", data=login_data)

# Check if login was successful
if "login" in login_res.url and login_res.status_code == 200:
    print("[!] Login failed! Please check your USERNAME and PASSWORD credentials.")
    exit(1)

# Table names updated as of 110926, update when needed
TABLES = [
    "scoreboard", "scoreboard-admin", "users+fields", "users+teams+fields",
    "teams+fields", "teams+members+fields", "notifications", "pages",
    "challenges", "hints", "awards", "tags", "topics", "challenge_topics",
    "solutions", "files", "flags", "users", "teams", "submissions",
    "solves", "unlocks", "tracking", "config", "tokens", "comments",
    "fields", "field_entries", "brackets", "audiences", "audience_members",
    "modules", "module_audience_access", "ratings"
]

print("3. Downloading CSVs...")

for table in TABLES:
    # Safely URL-encode the table parameter (e.g., converts 'users+fields' to 'users%2Bfields')
    encoded_table = urllib.parse.quote(table)
    target_url = f"{CTFD_URL}/admin/export/csv?table={encoded_table}"
    
    response = session.get(target_url)
    
    # Verify valid CSV response
    if response.status_code == 200 and not response.text.strip().startswith("<!DOCTYPE html>"):
        filepath = os.path.join(OUTPUT_DIR, f"{table}.csv")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f" -> Saved {table}.csv")
    else:
        print(f" -> Failed {table}.csv (Status: {response.status_code})")

print(f"\nDone! All CSVs saved to {OUTPUT_DIR}")