import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = 'centralautomationdashboard-cbcd913bcd93.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

sheet_url = "https://docs.google.com/spreadsheets/d/1Ny9W1xxsoycmFOJ6QFkYOmIm6zzYCwipAepbLXSsfhU/edit?gid=0#gid=0"
sheet = client.open_by_url(sheet_url).sheet1

print("First row:", sheet.row_values(1))
# Recommended (with named arguments, future-proof):
sheet.update(range_name='A1', values=[['Hello from Python!']])
print("Update successful!")
