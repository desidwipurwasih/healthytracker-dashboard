import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Nama file spreadsheet
SPREADSHEET_NAME = "HealthyTrackerData"

def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

def load_data():
    sheet = connect_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_data(row):
    sheet = connect_sheet()
    sheet.append_row(row)

def overwrite_data(df):
    sheet = connect_sheet()
    sheet.clear()
    sheet.append_row(df.columns.tolist())
    for row in df.values.tolist():
        sheet.append_row(row)
