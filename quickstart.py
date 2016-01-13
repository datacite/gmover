# https://developers.google.com/admin-sdk/groups-migration/v1/quickstart/python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import apiclient
from email import Utils
from email import MIMEText
import StringIO
import random

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/apps.groups.migration'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Apps Groups Migration API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'groupsmigration-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Admin-SDK Groups Migration API.

    Creates a Google Admin-SDK Groups Migration API service object and
    inserts a test email into a group.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('groupsmigration', 'v1', http=http)

    print('Warning: A test email will be inserted into the group entered.')
    groupId = raw_input(
        'Enter the email address of a Google Group in your domain: ')

    # Format an RFC822 message
    message = MIMEText.MIMEText('This is a test.')
    # Generate a random 10 digit number for message Id.
    message['Message-ID'] = '<{0}-{1}>'.format(str(random.randrange(10**10)),
                                               groupId)
    message['Subject'] = 'Groups Migration API Test (Python)'
    message['From'] = '"Alice Smith" <alice@example.com>'
    message['To'] = groupId
    message['Date'] = Utils.formatdate(localtime=True)

    stream = StringIO.StringIO()
    stream.write(message.as_string())
    media = apiclient.http.MediaIoBaseUpload(stream,
                                             mimetype='message/rfc822')

    result = service.archive().insert(groupId=groupId,
                                      media_body=media).execute()
    print(result['responseCode'])

if __name__ == '__main__':
    main()
