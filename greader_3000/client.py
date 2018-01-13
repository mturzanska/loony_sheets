import gspread
from oauth2client.service_account import ServiceAccountCredentials

from greader_3000 import config


class Client:

    SCOPE = ['https://spreadsheets.google.com/feeds']

    @classmethod
    def from_secret_json(cls, secret=None):
        secret = secret or config.SECRET
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            secret, cls.SCOPE)
        return cls(creds=creds)

    def __init__(self, creds):
        self.connection = self._get_connection(creds)

    def _get_connection(self, creds):
        return gspread.authorize(creds)
