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
        # TODO: Catch an exception on failed authorization
        self._client = gspread.authorize(creds)
        self.current_name = None
        self.current_gsheet = None

    def set_gsheet(self, gsheet_name):
        if self.current_name == gsheet_name:
            return
        try:
            self.current_gsheet = self._client.open(gsheet_name)
        except gspread.SpreadsheetNotFound:
            raise RuntimeError('Spreadsheet not found')
        self.current_name = gsheet_name

    def get_tab(self, tab_name):
        return self.current_gsheet.get_worksheet(tab_name)
