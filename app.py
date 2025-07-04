import streamlit as st
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="MoodMate – Daily Mood Tracker", layout="centered")

st.title("😊 MoodMate – Daily Mood Tracker")
st.write("Select your mood, get inspired, and track how you feel over time.")

# --- Setup --- #
moods = {
    "😊 Happy": {
        "quote": ["Happiness is a journey, not a destination.", "Smile more. Worry less."],
        "music": ["https://youtu.be/ZbZSe6N_BXs", "https://youtu.be/KQetemT1sWc"]
    },
    "😔 Sad": {
        "quote": ["Tough times don’t last, but tough people do.", "Crying is how your heart speaks when your lips can’t explain the pain."],
        "music": ["https://youtu.be/hLQl3WQQoQ0", "https://youtu.be/SfLV8hD7zX4"]
    },
    "😡 Angry": {
        "quote": ["Speak when you are angry and you will make the best speech you will ever regret.", "Control your anger before it controls you."],
        "music": ["https://youtu.be/04F4xlWSFh0", "https://youtu.be/AkFqg5wAuFk"]
    },
    "😴 Tired": {
        "quote": ["Rest is not idleness.", "Take time to recharge. You deserve it."],
        "music": ["https://youtu.be/2OEL4P1Rz04", "https://youtu.be/hHW1oY26kxQ"]
    }
}

# --- Mood selection --- #
st.subheader("🧠 How are you feeling today?")
selected_mood = st.selectbox("Select your mood", list(moods.keys()))

# --- Show quote & music --- #
if selected_mood:
    mood_data = moods[selected_mood]
    quote = random.choice(mood_data["quote"])
    music_link = random.choice(mood_data["music"])

    st.success(f"💬 Quote: *{quote}*")
    st.markdown(f"🎵 Music suggestion: [Click here to listen]({music_link})")

    # --- Journal entry --- #
    st.subheader("📝 Mood Journal")
    note = st.text_area("Write a few lines about your day")
    if st.button("Save Entry"):
        now = datetime.datetime.now()
        entry = pd.DataFrame([[now.date(), selected_mood, note]], columns=["Date", "Mood", "Note"])

        try:
            old_data = pd.read_csv("mood_log.csv")
            full_data = pd.concat([old_data, entry], ignore_index=True)
        except FileNotFoundError:
            full_data = entry

        full_data.to_csv("mood_log.csv", index=False)
        st.success("✅ Your entry has been saved!")

    # --- History / Chart --- #
    if st.checkbox("📊 Show Mood Chart"):
        try:
            df = pd.read_csv("mood_log.csv")
            mood_counts = df["Mood"].value_counts()

            fig, ax = plt.subplots()
            mood_counts.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_title("Mood Frequency Over Time")
            ax.set_ylabel("Count")
            st.pyplot(fig)
        except:
            st.warning("No mood data to show yet. Start journaling!")

# --- Footer --- #
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
