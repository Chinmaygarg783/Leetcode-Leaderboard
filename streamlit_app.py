import streamlit as st
import json
import os

# Initialize users list
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump([], f)  # Create empty file if missing

# Load existing users
with open("users.json", "r") as f:
    users = json.load(f)

# Streamlit UI
st.title("LeetCode User Manager")
new_user = st.text_input("Enter LeetCode Username")

if st.button("Add User") and new_user:
    if new_user not in users:
        users.append(new_user)
        with open("users.json", "w") as f:
            json.dump(users, f)  # Save updates
        st.success(f"Added {new_user}!")
    else:
        st.error("User already exists.")

# Display current users
st.write("Tracked Users:", users)

# Remove users
if users:
    user_to_remove = st.selectbox("Remove User", users)
    if st.button("Remove"):
        users.remove(user_to_remove)
        with open("users.json", "w") as f:
            json.dump(users, f)
        st.rerun()  # Refresh the app
