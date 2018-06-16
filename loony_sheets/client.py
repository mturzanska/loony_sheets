from loony_sheets.gsheets_wrapper import GsheetsClient
from loony_sheets.gsheets_wrapper import Sheet


class Connection:

    def __init__(self, gsheet_name):
        self._sheet = self._get_sheet(gsheet_name)
        self.cursor = self._cursor()

    @staticmethod
    def _get_sheet(gsheet_name):
        client = GsheetsClient.from_secret_json()
        raw_gsheet = client.open(gsheet_name)
        return Sheet(raw_gsheet)

    def close(self):
        self._gsheets_client = None
        self._cursor = None

    def commit(self):
        pass

    def _cursor(self):
        return Cursor(self._sheet)


class Cursor:

    def __init__(self, sheet):
        self._sheet = sheet
        self._description = None
        self._rowcount = -1
        self.arraysize = 1

    @property
    def description(self):
        return self._description

    @property
    def rowcount(self):
        return self._rowcount

    def close(self):
        self._gsheets_client = None

    def execute(self):
        pass

    def executemany(self):
        pass

    def fetchone(self):
        pass

    def fetchmany(self):
        pass

    def fetchall(self):
        pass

    def setinputsizes(self):
        pass

    def setinputsize(self):
        pass
