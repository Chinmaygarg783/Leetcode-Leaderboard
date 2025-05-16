
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

DRIVE_FILE = "data.json"

def fetch_user_stats(username):
    url = 'https://leetcode.com/graphql'
    query = '''
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    '''
    response = requests.post(url, json={'query': query, 'variables': {'username': username}})
    stats = response.json()['data']['matchedUser']['submitStats']['acSubmissionNum']
    return {
        'easy': next(s['count'] for s in stats if s['difficulty'] == 'Easy'),
        'medium': next(s['count'] for s in stats if s['difficulty'] == 'Medium'),
        'hard': next(s['count'] for s in stats if s['difficulty'] == 'Hard')
    }

@st.cache_data
def load_snapshot():
    with open(DRIVE_FILE, "r") as f:
        return json.load(f)

st.title("🏆 LeetCode Leaderboard")

if "users" not in st.session_state:
    st.session_state.users = ["user1", "user2"]

user_input = st.text_input("Add LeetCode Username:")
if st.button("Add User") and user_input:
    if user_input not in st.session_state.users:
        st.session_state.users.append(user_input)

remove_user = st.selectbox("Remove a user:", [""] + st.session_state.users)
if st.button("Remove User") and remove_user:
    st.session_state.users.remove(remove_user)

snapshot = load_snapshot()
today_str = datetime.utcnow().strftime('%Y-%m-%d')
week_ago = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')

leaderboard = []
week_stats = []

for user in st.session_state.users:
    today_stats = fetch_user_stats(user)
    prev_day = snapshot.get(today_str, {}).get(user, {"easy": 0, "medium": 0, "hard": 0})
    week_start = snapshot.get(week_ago, {}).get(user, {"easy": 0, "medium": 0, "hard": 0})

    today_diff = {
        'easy': today_stats['easy'] - prev_day['easy'],
        'medium': today_stats['medium'] - prev_day['medium'],
        'hard': today_stats['hard'] - prev_day['hard']
    }
    today_total = sum(v for v in today_diff.values())
    today_score = today_diff['easy'] * 1 + today_diff['medium'] * 3 + today_diff['hard'] * 5

    week_total = (
        (today_stats['easy'] - week_start['easy']) +
        (today_stats['medium'] - week_start['medium']) +
        (today_stats['hard'] - week_start['hard'])
    )

    leaderboard.append({
        "Username": user,
        "Easy": today_diff['easy'],
        "Medium": today_diff['medium'],
        "Hard": today_diff['hard'],
        "Total Solved Today": today_total,
        "Score Today": today_score
    })

    week_stats.append({
        "Username": user,
        "Total Solved This Week": week_total
    })

st.subheader("📅 Daily Leaderboard (Weighted Score)")
st.dataframe(pd.DataFrame(leaderboard).sort_values("Score Today", ascending=False).reset_index(drop=True))

st.subheader("🗓️ Weekly Leaderboard (Total Questions Solved)")
st.dataframe(pd.DataFrame(week_stats).sort_values("Total Solved This Week", ascending=False).reset_index(drop=True))
