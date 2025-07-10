from __future__ import print_function
import os.path
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': '手動測試建立事件',
        'description': '這是我自己測的事件',
        'start': {
            'dateTime': '2025-07-10T22:00:00+08:00',
            'timeZone': 'Asia/Taipei',
        },
        'end': {
            'dateTime': '2025-07-10T23:00:00+08:00',
            'timeZone': 'Asia/Taipei',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('✅ 建立成功：%s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()
