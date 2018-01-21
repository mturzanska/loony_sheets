import gspread
from oauth2client.service_account import ServiceAccountCredentials

from loony_sheets.config import SCOPE
from loony_sheets.config import SECRET


class Client:

    @classmethod
    def from_secret_json(cls, secret=SECRET, scope=SCOPE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            secret, scope)
        return cls(creds=creds)

    def __init__(self, creds):
        self.connection = self._get_connection(creds)

    def _get_connection(self, creds):
        return gspread.authorize(creds)
