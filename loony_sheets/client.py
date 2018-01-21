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
        self.connection = Connection(creds)


class Connection:

    def __init__(self, creds):
        self._gsheets_client = gspread.authorize(creds)
        self.cursor = self._cursor

    def close(self):
        self._gsheets_client = None
        self._cursor = None

    def commit(self):
        pass

    def _cursor(self):
        pass


class Cursor:

    def __init__(self, gsheets_client):
        self._gsheets_client = gsheets_client
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
