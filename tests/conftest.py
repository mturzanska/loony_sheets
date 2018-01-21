from pathlib import Path

import pytest

from loony_sheets import config


@pytest.fixture
def test_env(mocker):
    root_dir = Path('.').parent
    TEST_SECRET = Path(root_dir, 'client_secret.json')
    mocker.patch.object(config, 'SECRET', TEST_SECRET)
