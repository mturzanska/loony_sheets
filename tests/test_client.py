from pathlib import Path

import pytest
from oauth2client.client import HttpAccessTokenRefreshError

from greader_3000 import client
from greader_3000 import config


FAKE_CONNECTION = 'connection'
FAKE_CREDS = 'creds'


@pytest.mark.usefixtures('test_env')
class TestClient:

    def test_from_secret_json(self):
        a_client = client.Client.from_secret_json()
        assert a_client.connection

    def test_from_secret_json_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            client.Client.from_secret_json(FAKE_CREDS)

    def test_init(self, mocker):
        mocker.patch.object(client.Client, '_get_connection',
                            return_value=FAKE_CONNECTION)
        a_client = client.Client(creds=FAKE_CREDS)

        assert a_client.connection == FAKE_CONNECTION
        a_client._get_connection.assert_called_once_with(FAKE_CREDS)

    def test__get_connection(self):
        a_client = client.Client.from_secret_json(
                config.SECRET)
        assert a_client.connection

    def test__get_connection_wrong_key(self, mocker):
        root_dir = Path('.').parent
        TEST_SECRET = Path(root_dir, 'wrong_key_secret.json')
        mocker.patch.object(config, 'SECRET', TEST_SECRET)
        with pytest.raises(HttpAccessTokenRefreshError):
            client.Client.from_secret_json(config.SECRET)
