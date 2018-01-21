from loony_sheets.client import Client


def connect():
    client = Client.from_secret_json()
    return client.connection
