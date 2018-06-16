from collections import defaultdict

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from loony_sheets.config import SCOPE
from loony_sheets.config import SECRET


class GsheetsClient:
    # Humble object, hopefully

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
            return self._client.open(name)
        except gspread.SpreadsheetNotFound:
            raise RuntimeError('Sheet not found')


class Sheet:

    def __init__(self, raw_sheet):
        self._gsheet = raw_sheet
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
            raw_tab = self._gsheet.get_worksheet(tab_idx)
            tab = Tab(raw_tab)
        except Exception as e:
            print(e)
            # TODO: check which exceptions to catch
            raise RuntimeError('Tab not found')

        self._tabs_cache[tab_name] = tab
        return tab


class Tab:

    def __init__(self, raw_tab):
        self._raw_tab = raw_tab
        self.columns = self._get_columns()

    def _get_columns(self):
        columns_raw = defaultdict(list)
        columns = {}

        for row in self._raw_tab.get_all_records():
            for key, value in row.items():
                columns_raw[key].append(value)

        for col_name, data in columns_raw.items():
            columns[col_name] = Column(col_name, data)

        return columns


class Column:

    def __init__(self, name, values):
        self.name = name
        self.values = values

    def select_by_idx(by_idx):
        pass

    def find_idx_where(condition):
        pass
