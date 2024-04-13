import json

from datetime import datetime

from telethon.sync import TelegramClient

from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import GetHistoryRequest


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Telegram_Parser:

    @classmethod
    def client_initialize(cls):
        api_id = int(input('Enter app_id: '))  # 11111111
        api_hash = str(input('Enter app_hash: '))  # '11111111111111111111111111111111'
        phone = str(input('Enter phone number: '))  # '11111111111'
        return api_id, api_hash, phone

    @classmethod
    def client_start(cls, api_id, api_hash, phone):
        try:
            client = TelegramClient(phone, api_id, api_hash, system_version="4.16.30-vxCUSTOM")
            client.start()

            return client
        except Exception:
            raise Exception("Указан неправильный токен")

    def __init__(self):
        self.api_id, self.api_hash, self.phone = self.client_initialize()
        self.client = self.client_start(self.api_id, self.api_hash, self.phone)
        pass

    def client_is_connected(self):
        return self.client.is_connected()

#    async def parse_channel(self, url, path_to_json="channel_messages.json", offset_id=0, limit=100,
#                            total_count_limit=50):
#        channel = await client.get_entity(url)
#
#        all_messages = []
#        total_messages = 0
#
#        while True:
#            history = await client(GetHistoryRequest(
#                peer=channel,
#                offset_id=offset_id,
#                offset_date=None,
#                add_offset=0,
#                limit=limit,
#                max_id=0,
#                min_id=0,
#                hash=0
#            ))
#            if not history.messages:
#                break
#            messages = history.messages
#            for message in messages:
#                all_messages.append(message.to_dict())
#            offset_id = messages[len(messages) - 1].id
#            total_messages = len(all_messages)
#            if total_count_limit != 0 and total_messages >= total_count_limit:
#                break

#        with open("channel_messages.json", "w", encoding="UTF-8") as outfile:
#            json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

#    async def client_disconnect(self):
#        await client.disconnect()