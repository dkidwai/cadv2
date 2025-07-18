import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'centralautomationdashboard-cbcd913bcd93.json'

# Use both Sheets and Drive scopes!
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Main Spreadsheet name (or spreadsheet ID)
SHEET_NAME = 'CentralAutomationDB'

# Authorize gspread client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

def get_sheet(sheet_name):
    """Return the worksheet object, create it if not exists."""
    sh = client.open(SHEET_NAME)
    try:
        ws = sh.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=sheet_name, rows="1000", cols="20")
    return ws

@st.cache_data(ttl=180)  # cache for 3 minutes, reduce API quota issues
def load_sheet_from_db(sheet_name):
    """Load data from Google Sheet worksheet into pandas DataFrame."""
    ws = get_sheet(sheet_name)
    data = ws.get_all_values()
    if not data or len(data) < 2:
        return pd.DataFrame()
    header, *values = data
    df = pd.DataFrame(values, columns=header)
    return df

def save_sheet_to_db(sheet_name, df):
    """Save pandas DataFrame to Google Sheet worksheet (replace all data)."""
    ws = get_sheet(sheet_name)
    ws.clear()
    # Set header
    ws.append_row(df.columns.tolist())
    # Set values
    rows = df.astype(str).values.tolist()
    if rows:
        ws.append_rows(rows)
    # Invalidate Streamlit cache so new data shows up immediately
    load_sheet_from_db.clear(sheet_name)
