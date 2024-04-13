import pytest
from unittest.mock import patch
from TG_parser import Telegram_Parser
from contextlib import nullcontext as does_not_raise


class Tester:
    @pytest.mark.parametrize(
        'api_id, api_hash, phone, res, expectation',
        [
            (11111111, '11111111111111111111111111111111', '11111111111', True, does_not_raise()),  # Enter Normal Data
            (11111111, '11111111111111111111111111111111', '11111111111', None, pytest.raises(Exception)),
            (None, None, None, None, pytest.raises(Exception))

        ]
    )
    def test_client_autorization(self, api_id, api_hash, phone, res, expectation):
        with expectation:
            assert Telegram_Parser().client_start(api_id=api_id, api_hash=api_hash, phone=phone).is_connected()


    def test_client_initialize(self):
        assert Telegram_Parser().client_initialize()