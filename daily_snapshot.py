import json
import datetime
from fetch_leetcode_data import get_user_stats  # Assuming you have a function for this

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_snapshot():
    today = str(datetime.date.today())
    data = load_data()

    for username in data:
        stats = get_user_stats(username)
        today_count = stats.get("solved_problems", 0)

        # Append today's snapshot if not already present
        history = data[username].get("history", [])
        if not history or history[-1]["date"] != today:
            history.append({"date": today, "solved": today_count})
            data[username]["history"] = history

    save_data(data)

if __name__ == "__main__":
    update_snapshot()
