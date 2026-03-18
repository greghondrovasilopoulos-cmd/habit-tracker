import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta, datetime

# -------------------------------
# File paths (works locally or in Replit)
DATA_FILE = "habit_mood_data.csv"
USER_FILE = "user_stats.csv"

# -------------------------------
# Initialize files if they don't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Habit", "Completed", "Mood", "Quantity", "Goal"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

if not os.path.exists(USER_FILE):
    user = pd.DataFrame([{"XP": 0, "Level": 1}])
    user.to_csv(USER_FILE, index=False)
else:
    user = pd.read_csv(USER_FILE)

# -------------------------------
st.set_page_config(page_title="Habit Tracker", layout="centered")
st.title("Habit & Mood Tracker 🌟")

# -------------------------------
# Tabs for a cleaner app layout
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "➕ Add Entry", "📊 Progress"])

# -------------------------------
# Tab 1: Dashboard
with tab1:
    st.subheader("🏆 Your Stats")
    st.write(f"Level: {user['Level'][0]}")
    st.write(f"XP: {user['XP'][0]}")

    # Daily Score
    st.subheader("📊 Daily Score")
    today = date.today().isoformat()
    today_df = df[df["Date"] == today]
    if not today_df.empty:
        completed_today = today_df[today_df["Completed"] == "Yes"].shape[0]
        total_today = today_df.shape[0]
        score = int((completed_today / total_today) * 100) if total_today > 0 else 0
        st.progress(score / 100)
        st.write(f"{score}% Complete")
    else:
        st.write("No entries today yet.")

# -------------------------------
# Tab 2: Add Entry
with tab2:
    st.subheader("➕ Add Habit Entry")
    
    # Habit options
    common_habits = ["Drink Water", "Exercise", "Meditate", "Read", "Sleep 7+ hours", "Other"]
    habit_choice = st.selectbox("Select Habit", common_habits)
    if habit_choice == "Other":
        habit = st.text_input("Custom Habit")
    else:
        habit = habit_choice
    
    completed = st.radio("Completed?", ("Yes", "No"))
    mood = st.slider("Mood (1=bad, 5=great)", 1, 5, 3)
    quantity = st.number_input("Amount (optional)", min_value=0.0, step=0.1)
    goal = st.number_input("Daily Goal (optional)", min_value=0.0, step=0.1)

    if st.button("Save Entry"):
        if habit.strip() == "":
            st.error("Please enter a habit!")
        else:
            new_entry = pd.DataFrame({
                "Date": [date.today().isoformat()],
                "Habit": [habit],
                "Completed": [completed],
                "Mood": [mood],
                "Quantity": [quantity],
                "Goal": [goal]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            # XP system
            if completed == "Yes":
                user["XP"][0] += 10
                if user["XP"][0] >= user["Level"][0] * 100:
                    user["Level"][0] += 1
                    st.success("🎉 Level Up!")
                user.to_csv(USER_FILE, index=False)

            st.success("Entry saved!")

# -------------------------------
# Tab 3: Progress
with tab3:
    st.subheader("📈 Mood Trend")
    if not df.empty:
        mood_df = df.groupby("Date")["Mood"].mean()
        st.line_chart(mood_df)
    else:
        st.write("No data yet.")

    st.subheader("🔥 Streaks")
    streaks = {}
    for habit_name in df["Habit"].unique():
        habit_df = df[df["Habit"] == habit_name].sort_values("Date")
        current_streak = 0
        max_streak = 0
        prev_date = None
        for _, row in habit_df.iterrows():
            entry_date = pd.to_datetime(row["Date"]).date()
            if row["Completed"] == "Yes":
                if prev_date and entry_date == prev_date + timedelta(days=1):
                    current_streak += 1
                else:
                    current_streak = 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
            prev_date = entry_date
        streaks[habit_name] = max_streak
    st.write(streaks)

# -------------------------------
# Premium Upsell
st.markdown("---")
st.subheader("🔒 Premium Features")
st.write("""
- Detailed habit tracking (amounts, goals)
- Streak tracking 🔥
- Advanced analytics 📊
- No ads
""")
if st.button("Upgrade (Coming Soon)"):
    st.success("🚀 Premium feature coming soon!")