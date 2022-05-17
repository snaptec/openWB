from unittest.mock import Mock

import pytest
from modules.common import simcount


@pytest.fixture(autouse=True)
def mock_simcount(monkeypatch):
    monkeypatch.setattr(simcount.SimCount, 'sim_count', Mock(return_value=(100, 200)))
    monkeypatch.setattr(simcount.SimCountLegacy, 'sim_count', Mock(return_value=(100, 200)))
