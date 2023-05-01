import google.auth.transport.requests as g_requests
import google.oauth2.credentials as g_credentials
from google.oauth2.credentials import Credentials
import google_auth_oathlib.flow as g_flow
import googleapiclient.discovery as g_discovery
import googleapiclient.errors as g_errors

import os.path

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = g_credentials.Credentials.from_authorized_user_file("token.json", SCOPES)
