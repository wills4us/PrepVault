import pandas as pd
import os
from datetime import datetime, timedelta
import streamlit as st
import random

ACTIVITY_FILE = "user_activity.csv"
NOTIFICATION_FILE = "notifications.txt"

def check_and_generate_notifications():
    # Ensure the activity file exists
    if not os.path.exists(ACTIVITY_FILE) or os.stat(ACTIVITY_FILE).st_size == 0:
        df = pd.DataFrame(columns=["username", "timestamp", "action"])
        df.to_csv(ACTIVITY_FILE, index=False)
        return  # No activity data yet

    df = pd.read_csv(ACTIVITY_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    recent_cutoff = datetime.now() - timedelta(days=3)

    # Filter users with no activity in the last 3 days
    latest_activity = df.sort_values("timestamp").drop_duplicates("username", keep="last")
    inactive_users = latest_activity[latest_activity["timestamp"] < recent_cutoff]["username"].unique()

    # Load previous notifications to avoid duplicates
    existing_notes = []
    if os.path.exists(NOTIFICATION_FILE):
        with open(NOTIFICATION_FILE, "r") as f:
            existing_notes = f.readlines()

    # Create notification messages
    templates = [
        "👀 Hey {user}, we've missed you! Resume your career prep today!",
        "🕒 {user}, it's been a while. How about a quick study session?",
        "🚀 Ready to make progress again, {user}? Let's go!",
        "📚 {user}, your growth journey is waiting. Jump back in!"
    ]

    new_notifications = []
    for user in inactive_users:
        if not any(user in note for note in existing_notes):
            message = random.choice(templates).format(user=user)
            new_notifications.append(message)

    # Append new notifications
    if new_notifications:
        with open(NOTIFICATION_FILE, "a") as f:
            for note in new_notifications:
                f.write(note + "\n")


def show_notifications(username):
    if not os.path.exists(NOTIFICATION_FILE):
        st.info("🔕 No new notifications.")
        return

    with open(NOTIFICATION_FILE, "r") as f:
        lines = f.readlines()

    # Match only full username mentions
    user_notifications = [line.strip() for line in lines if f"{username}" in line.split(" ")[-1]]

    if user_notifications:
        for note in user_notifications:
            st.success(note)
    else:
        st.info("✅ You're all caught up!")
