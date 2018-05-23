import gspread
from oauth2client.service_account import ServiceAccountCredentials

from loony_sheets.config import SCOPE
from loony_sheets.config import SECRET


class GsheetsWrapper:

    @classmethod
    def from_secret_json(cls, secret=SECRET, scope=SCOPE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            secret, scope)
        return cls(creds=creds)

    def __init__(self, creds):
        self._client = gspread.authorize(creds)

    def get_contents(self, gsheet_name):
        return self._client.open('Greader3000_sample_sheet')
