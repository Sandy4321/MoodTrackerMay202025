# MoodTrackerMay202025
# Streamlit Mood Tracker 😊😠😕

A simple web app to log your mood and notes.  
Data is saved **locally in Excel** and optionally **to Google Sheets** for cloud access.

---

## Features

- Select your mood from emojis (😊 😠 😕 🎉)
- Add an optional note
- Log entries with a timestamp
- View your full timesheet (in-app, Excel, or Google Sheets)
- Visualize today's mood counts as a bar chart (matplotlib)
- Data stored in `mood_timesheet.xlsx` (local) and Google Sheets (optional)

---

## Requirements

- Python 3.8+
- `streamlit`
- `pandas`
- `openpyxl`
- `matplotlib`
- (Optional, for Google Sheets sync) `gspread`, `gspread_dataframe`, `google-auth`

Install dependencies with:
```bash
pip install streamlit pandas openpyxl matplotlib gspread gspread_dataframe google-auth


## Usage
Select your mood and optionally add a note.

Click "Submit" to log the entry.

Use "Show Mood Chart" to visualize mood counts for today.

View all entries in-app or directly in the Excel/Google Sheet.

## Files
app.py — Main Streamlit app code

mood_timesheet.xlsx — Local data log (auto-created)
