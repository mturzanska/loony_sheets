import gspread
from oauth2client.service_account import ServiceAccountCredentials

from loony_sheets.config import SCOPE
from loony_sheets.config import SECRET


class GsheetsClient:

    @classmethod
    def from_secret_json(cls, secret=SECRET, scope=SCOPE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            secret, scope)
        return cls(creds=creds)

    def __init__(self, creds):
        # TODO: Catch an exception on failed authorization
        self._client = gspread.authorize(creds)

    def open(self, name):
        try:
            return Sheet(self._client, name)
        except gspread.SpreadsheetNotFound:
            raise RuntimeError('Sheet not found')


class Sheet:

    def __init__(self, client, name):
        self.name = name
        self._gsheet = client.open(name)
        self._tabs_map = self.map_tabs()
        self.tabs = list(self._tabs_map.keys())
        self._tabs_cache = {}

    def map_tabs(self):
        tabs_map = {}
        tabs = self._gsheet.worksheets()
        for idx, tab in enumerate(tabs):
            tabs_map[tab.title] = idx
        return tabs_map

    def get_tab(self, tab_name):
        if tab_name in self._tabs_cache:
            return self._tabs_cache.get(tab_name)
        tab_idx = self._tabs_map.get(tab_name)

        try:
            tab = self._gsheet.get_worksheet(tab_idx)
        except Exception:
            # TODO: check which exceptions to catch
            raise RuntimeError('Tab not found')

        self._tabs_cache[tab_name] = tab
        return tab


class Tab:

    pass
