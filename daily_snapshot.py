import json
import requests
from datetime import datetime

# ✅ Replace these with your actual LeetCode usernames
USERS = [
    "your_friend1",
    "your_friend2",
    "your_username"
]

LEETCODE_API = "https://leetcode-stats-api.herokuapp.com/{}"

DATA_FILE = "data.json"

# Load existing data
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

today = datetime.utcnow().strftime("%Y-%m-%d")
data[today] = {}

for username in USERS:
    url = LEETCODE_API.format(username)
    r = requests.get(url)
    if r.status_code == 200:
        stats = r.json()
        data[today][username] = {
            "easy": stats.get("easySolved", 0),
            "medium": stats.get("mediumSolved", 0),
            "hard": stats.get("hardSolved", 0)
        }

# Save updated data
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)