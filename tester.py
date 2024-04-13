import pytest
import os
import pandas as pd
from unittest.mock import patch
from parser_telegram_class import Telegram_Parser
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
            assert Telegram_Parser(api_id=api_id, api_hash=api_hash, phone=phone).client_start(phone=phone, api_id=api_id, api_hash=api_hash).is_connected() == res

    @pytest.mark.parametrize(
        'api_id, api_hash, phone, url, expectation',
        [
            (11111111, '11111111111111111111111111111111', '11111111111', "https://t.me/rian_ru", True, does_not_raise()),  # Enter Normal Data
            (11111111, '11111111111111111111111111111111', '11111111111', None, None, pytest.raises(Exception)),
            (None, None, None, None)
        ]
    )
    def test_json_file_creating(self, api_id, api_hash, phone, url, res, expectation):
        with expectation:
            Telegram_Parser(api_id=api_id, api_hash=api_hash, phone=phone).parse_channel(url=url)
            df = pd.read_json("channel_messages.json")
            assert df.shape[0] > 0 == res

    def test_json_file_columns_num(self):
        assert len(pd.read_json("channel_messages.json").columns) == 33

    def test_json_columns_types(self):
        dict = {"_": "object", "id": "int64", "peer_id": "object", "date": "datetime64[ns, UTC]", "message": "object",
                "out": "bool", "mentioned": "bool", "media_unread": "bool", "silent": "bool", "post": "bool",
                "from_scheduled": "bool", "legacy": "bool", "edit_hide": "bool", "pinned": "bool", "noforwards": "bool",
                "invert_media": "bool", "from_id": "float64", "saved_peer_id": "float64", "fwd_from": "float64",
                "via_bot_id": "float64", "reply_to": "object", "media": "object", "reply_markup": "float64",
                "entities": "object", "views": "int64", "forwards": "int64", "replies": "float64",
                "edit_date": "object",
                "post_author": "float64", "grouped_id": "float64", "reactions": "float64",
                "restriction_reason": "object",
                "ttl_period": "float64"}
        df = pd.read_json("channel_messages.json")
        dict_df = df.dtypes
        flag = True
        for key in dict:
            if dict[key] != dict_df[key]:
                flag = False
        assert flag == True

    def test_not_null_messages(self):
        df = pd.read_json("channel_messages.json")
        nans_in_messages = df["message"].isna().sum()
        assert nans_in_messages < df.shape[0] * 0.1
