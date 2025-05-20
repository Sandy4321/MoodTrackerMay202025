import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- Google Sheets setup ---
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# Google Sheet config
GOOGLE_SHEET_NAME = "mood_timesheet"  # Or your sheet name
CREDS_FILE = "creds.json"  # Your downloaded service account file

def append_to_gsheet(df_new):
    try:
        # Define scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scope)
        gc = gspread.authorize(creds)

        # Open sheet and worksheet
        sh = gc.open(GOOGLE_SHEET_NAME)
        worksheet = sh.sheet1

        # Get current data, append new, and re-upload
        existing = pd.DataFrame(worksheet.get_all_records())
        df_all = pd.concat([existing, df_new], ignore_index=True) if not existing.empty else df_new
        worksheet.clear()
        set_with_dataframe(worksheet, df_all)
    except Exception as e:
        st.warning(f"Could not update Google Sheet: {e}")

st.title("Mood Tracker 😊😠😕🎉")

# Emoji-mood pairs
mood_emojis = {
    "Happy 😊": "😊",
    "Angry 😠": "😠",
    "Confused 😕": "😕",
    "Celebrating 🎉": "🎉"
}

# Dropdown for mood selection
mood = st.selectbox("Select your mood:", list(mood_emojis.keys()))
note = st.text_input("Add a note (optional):")

file_path = "mood_timesheet.xlsx"

if st.button("Submit"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mood_symbol = mood_emojis[mood]

    # DataFrame for this entry
    df_new = pd.DataFrame([{
        'Timestamp': timestamp,
        'Mood': mood_symbol,
        'Note': note
    }])

    # Local Excel update
    if os.path.exists(file_path):
        df_old = pd.read_excel(file_path)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_excel(file_path, index=False)

    # Google Sheets update
    append_to_gsheet(df_new)

    st.success("Mood logged! 🎯")

    with st.expander("Show timesheet (local Excel)"):
        st.dataframe(df_all)

# --- Visualization Part ---
st.markdown("---")
if st.button("Show Mood Chart"):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        today = datetime.now().strftime('%Y-%m-%d')
        df['Date'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%d')
        df_today = df[df['Date'] == today]

        if not df_today.empty:
            mood_counts = df_today['Mood'].value_counts().reindex(mood_emojis.values(), fill_value=0)
            fig, ax = plt.subplots()
            bars = ax.bar(mood_counts.index, mood_counts.values, color=['gold', 'red', 'gray', 'limegreen'])
            ax.set_title("Today's Mood Counts")
            ax.set_xlabel("Mood")
            ax.set_ylabel("Count")
            ax.set_ylim(0, max(mood_counts.values.max(), 1))
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')
            st.pyplot(fig)
        else:
            st.info("No mood entries for today yet!")
    else:
        st.info("No data found. Log some moods first!")
