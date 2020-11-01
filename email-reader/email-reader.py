from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pyttsx3

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class EmailReader:

    credens = None
    service = None
    engine = pyttsx3.init()
    index = 1

    def __init__(self):
        self.auth()

    def auth(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credens = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credens or not credens.valid:
            if credens and credens.expired and credens.refresh_token:
                credens.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credens = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credens, token)

        self.service = build('gmail', 'v1', credentials=credens)
        self.get_email(self.service)

        # Call the Gmail API
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])
        #
        # # print(labels)
        #
        # if not labels:
        #     print('No labels found.')
        # else:
        #     print('Labels:')
        #     for label in labels:
        #         print(label['name'])

    def get_email(self, service):
        messages_obj = service.users().messages().list(userId='me').execute()
        messages = messages_obj.get('messages')
        msg = messages[self.index]
        self.read_email(msg['id'], service)

    def read_email(self, email_id, service):
        email_obj = service.users().messages().get(userId='me', id=email_id).execute()
        part = email_obj['payload']['parts'][0]
        msg = part['body']['data']
        output = base64.urlsafe_b64decode(msg)
        output = str(output).replace('\\r', '').replace('\\n', '. ')
        output = output.split('. ')
        output = output[1:6]
        self.tts_email(output, self.engine)

    def tts_email(self, msg, engine):
        # engine = pyttsx3.init()
        # print(msg)
        output = ' '
        for word in msg:
            output += str(word) + '. '

        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-15)
        engine.say(f'Email {self.index}')
        print(f'Email {self.index}')
        engine.say(output)
        print(output)
        engine.runAndWait()
        self.next_email()

    def next_email(self):
        self.engine.say('Do you want to continue? ')
        self.engine.runAndWait()
        continue_check = str(input('Do you want to continue? '))
        if continue_check.lower() == 'y' or continue_check.lower() == 'yes':
            self.index += 1
            self.get_email(self.service)
        else:
            self.engine.say('Thanks for trying the Email Reader. ')
            print('Thanks for trying the Email Reader. ')
            self.engine.runAndWait()


email = EmailReader()

