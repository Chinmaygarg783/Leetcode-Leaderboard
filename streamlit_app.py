import streamlit as st
import json
import datetime

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def get_stats_by_range(data, days_back):
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=days_back)

    delta_stats = []
    for user, info in data.items():
        history = info.get("history", [])
        today_solved = None
        past_solved = None

        for entry in reversed(history):
            date = datetime.date.fromisoformat(entry["date"])
            if date == today:
                today_solved = entry["solved"]
            if date == cutoff:
                past_solved = entry["solved"]

        if today_solved is not None and past_solved is not None:
            delta_stats.append((user, today_solved - past_solved))

    delta_stats.sort(key=lambda x: x[1], reverse=True)
    return delta_stats

st.title("Leetcode Leaderboard")

mode = st.radio("Select Ranking Mode", ["All-Time", "Weekly", "Daily"])
data = load_data()

if mode == "All-Time":
    all_time = [(user, info["history"][-1]["solved"]) for user, info in data.items()]
    all_time.sort(key=lambda x: x[1], reverse=True)
    st.write("### All-Time Leaderboard")
    st.table(all_time)

elif mode == "Weekly":
    weekly = get_stats_by_range(data, 7)
    st.write("### Weekly Leaderboard")
    st.table(weekly)

elif mode == "Daily":
    daily = get_stats_by_range(data, 1)
    st.write("### Daily Leaderboard")
    st.table(daily)
