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

    global client, phone
    
    def __init__(self) -> None:
        pass
    
    def client_initialize():
        api_id   = int(input('Enter app_id: ')) #11111111
        api_hash = str(input('Enter app_hash: ')) #'11111111111111111111111111111111'
        phone    = str(input('Enter phone number: ')) #'11111111111'
        client   = TelegramClient(phone, api_id, api_hash, system_version = "4.16.30-vxCUSTOM")
        return api_id, api_hash, phone
    
    async def client_start():
        await client.start()

        if not client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password = input('Password: '))

    async def parse_channel(url, path_to_json = "channel_messages.json", offset_id = 0, limit = 100, total_count_limit = 50):
        channel = await client.get_entity(url)

        all_messages = []
        total_messages = 0
        
        while True:
            history = await client(GetHistoryRequest(
                peer        = channel,
                offset_id   = offset_id,
                offset_date = None,
                add_offset  = 0,
                limit       = limit,
                max_id      = 0,
                min_id      = 0,
                hash        = 0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        
        with open(path_to_json, "w", encoding="UTF-8") as outfile:
            json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

    async def client_disconnect():
        await client.disconnect()