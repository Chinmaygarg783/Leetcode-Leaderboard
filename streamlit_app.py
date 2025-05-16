import streamlit as st
import json
import os

# Initialize users.json if it doesn't exist
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump([], f)  # Create empty list

# Load existing users
with open("users.json", "r") as f:
    users = json.load(f)

# Streamlit UI
st.title("LeetCode User Manager")

# Add User Section
new_user = st.text_input("Enter LeetCode Username")
if st.button("Add User") and new_user:
    if new_user not in users:
        users.append(new_user)
        with open("users.json", "w") as f:
            json.dump(users, f)  # Save to file
        st.success(f"Added {new_user}!")
        st.rerun()  # Refresh to show changes
    else:
        st.error("User already exists!")

# Remove User Section
if users:
    st.subheader("Current Users")
    selected_user = st.selectbox("Select user to remove", users)
    if st.button("Remove Selected User"):
        users.remove(selected_user)
        with open("users.json", "w") as f:
            json.dump(users, f)
        st.success(f"Removed {selected_user}!")
        st.rerun()

# Display all users
st.write("## All Tracked Users")
st.json(users)
