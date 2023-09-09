
import base64
from custom import CREDENTIALS, KEYFILE, SCOPES, USER, SHEET_ID
import email

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import gspread
import os
import pickle
import requests
import time

def gmail_authenticate():
    #Reference: https://developers.google.com/gmail/api/quickstart/python
    print('getting gmail service..')
    
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def Sheets():
    print('getting google sheets service..')
    return gspread.service_account(filename=KEYFILE)

def search_history(startHistoryId, decoy):
    print(f'search history for id = {startHistoryId}')
    time.sleep(30) #newly created history ids needs time to be accessed from GMail API, thus the delay here

    log_row = [ startHistoryId ]
    
    service = gmail_authenticate()
    result = service.users().history().list(userId='me',startHistoryId=startHistoryId).execute() #you can also use USER instead of 'me'

    if "history" in result:
        print('history in result')

        msg_ids = []
        history:list[dict] = result['history'] #messages are in chronological order
        for h in history: 
            id = h['messages'][0]['id']

            if id not in msg_ids: #only process unique ids to save time
                msg_ids.append(id)
                try:
                    r = service.users().messages().get(userId='me', id=id, format='raw').execute() # reference: https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get
                except Exception as e: #message_id may be invalid
                    time.sleep(5)
                    continue
                
                #get the snippet and label
                snippet = r['snippet']
                
                mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(r['raw']))

                #get the date
                day = mime_msg['date']

                #get recipient's email address
                recipient = mime_msg['to']
                if '<' in recipient:
                    recipient = recipient[recipient.find('<')+1:recipient.find('>')]

                #get subject
                subject = mime_msg['subject']

                #get the body
                body = None
                message_main_type = mime_msg.get_content_maintype()
                if message_main_type == 'multipart':
                    for part in mime_msg.get_payload():
                        if part.get_content_maintype() == 'text':
                            payload = part.get_payload()
                            if '<div' not in payload:
                                body = payload
                elif message_main_type == 'text':
                    payload = mime_msg.get_payload()
                    if "<div" not in payload:
                        body = payload
                    
                log_row += [ id, day, recipient, subject, snippet, body ]
                print(log_row)

                try:
                    ss = Sheets()
                    tab = ss.open_by_key(SHEET_ID).worksheet('Sheet 1')
                    tab.append_row(log_row)
                except Exception as e:
                    print(f'Error writing in sheet! Error = {e}')
                
                break
    else:
        print('No history found')

if __name__ == '__main__':
    gmail_authenticate()