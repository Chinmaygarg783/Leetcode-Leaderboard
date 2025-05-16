import streamlit as st
import json
from datetime import datetime, timedelta

DATA_FILE = "data.json"
POINTS = {"easy": 1, "medium": 3, "hard": 5}

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def compute_today_stats(data):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    today_stats = {}

    if today in data and yesterday in data:
        for user in data[today]:
            today_stats[user] = {
                diff: data[today][user][diff] - data[yesterday].get(user, {}).get(diff, 0)
                for diff in POINTS
            }
    return today_stats

def compute_weekly_stats(data):
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = datetime.utcnow().strftime("%Y-%m-%d")
    week_stats = {}

    for date in data:
        if week_ago <= date <= today:
            for user in data[date]:
                if user not in week_stats:
                    week_stats[user] = {k: 0 for k in POINTS}
                for diff in POINTS:
                    week_stats[user][diff] += data[date][user][diff]
    return week_stats

def calculate_points(stats):
    return {
        user: sum(count * POINTS[diff] for diff, count in stat.items())
        for user, stat in stats.items()
    }

data = load_data()
today_stats = compute_today_stats(data)
weekly_stats = compute_weekly_stats(data)

today_points = calculate_points(today_stats)
weekly_points = calculate_points(weekly_stats)

st.title("📊 LeetCode Leaderboard")

st.header("🏆 Today's Ranking")
today_sorted = sorted(today_points.items(), key=lambda x: x[1], reverse=True)
for i, (user, points) in enumerate(today_sorted, 1):
    st.write(f"**{i}. {user}** — {points} pts")

st.header("📈 Weekly Ranking")
weekly_sorted = sorted(weekly_points.items(), key=lambda x: x[1], reverse=True)
for i, (user, points) in enumerate(weekly_sorted, 1):
    st.write(f"**{i}. {user}** — {points} pts")

st.header("📅 Problems Solved Today")
for user, stats in today_stats.items():
    st.write(f"**{user}**: {stats}")