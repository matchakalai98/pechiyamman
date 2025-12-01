import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
FOLDER_ID = '1oUezkIPpYjs901ROtJUWYKtlZjOsBgdL'

def create_monthly_sheet_and_append(data):
    month_year = datetime.now().strftime("%B_%Y")
    sheet_name = f"Invoices_{month_year}"

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)

    # Check if sheet already exists in the folder
    query = f"'{FOLDER_ID}' in parents and name='{sheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if files:
        spreadsheet_id = files[0]['id']
    else:
        file_metadata = {
            'name': sheet_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [FOLDER_ID]
        }
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        spreadsheet_id = file.get('id')
        # Set up header row
        header = [['Customer name', 'Phone', 'Bike number', 'Total']]
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1:D1',
            valueInputOption='RAW',
            body={'values': header}
        ).execute()

    # Append data
    sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='A2',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': data}
    ).execute()

    print(f"Sheet updated! Link: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")