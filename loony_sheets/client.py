from loony_sheets.gsheets_wrapper import GsheetsClient


class Connection:

    def __init__(self):
        self._gsheets_client = GsheetsClient.from_secret_json()
        self.cursor = self._cursor()

    def close(self):
        self._gsheets_client = None
        self._cursor = None

    def commit(self):
        pass

    def _cursor(self):
        return Cursor(self._gsheets_client)


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
