from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import asyncio
import sqlite3

def main(argv):
    if sys.argv[6] == '0':
        entity = 'AudioTube_bot'
    else:
        entity = 'AudioTube_bot'+str(sys.argv[7])
    api_id = 123456
    api_hash = 'xxxxxxxxxxxxxxxxx'
    phone = '+3800000000'
    client = TelegramClient(entity, api_id, api_hash)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())
    if not loop.run_until_complete(client.is_user_authorized()):
        #client.send_code_request(phone) #при первом запуске - раскомментить, после авторизации для избежания FloodWait советую закомментить
        client.sign_in(phone, input('Enter code: '))
    try:
        client.start()
    except sqlite3.OperationalError:
        for x in range(4):
            client = TelegramClient('AudioTube_bot'+str(x), api_id, api_hash)
            client.connect()
            if not client.is_user_authorized():
                #client.send_code_request(phone) #при первом запуске - раскомментить, после авторизации для избежания FloodWait советую закомментить
                client.sign_in(phone, input('Enter code: '))
            try:
                client.start()
                break
            except sqlite3.OperationalError:
                continue
    file_path = argv[1]
    file_name = argv[10]
    print(file_name)
    chat_id = argv[2]
    object_id = argv[3]
    bot_name = argv[4]
    duration = argv[5]
    size = argv[7]
    msid = argv[8]
    msid2 = argv[9]
    thumbnail = argv[11]
    loop = asyncio.get_event_loop()
    msg = loop.run_until_complete(client.send_file(
                           str(bot_name),
                           file_path,
                           caption=str('{\'chat_id\': \'' + chat_id + '\', \'ytid\': \''
                                       + object_id + '\', \'size\': \'' + size + '\', \'ms_id\': \''
                                       + msid + '\', \'name\': "' + file_name + '", \'ms_id2\': \'' + msid2 + '\','
                                       ' \'thumbnail\': \'' + thumbnail + '\'}'),
                           file_name=str(file_name),
                           use_cache=False,
                           part_size_kb=512,
                           attributes=[DocumentAttributeAudio(
                                                      int(duration),
                                                      voice=None,
                                                      title=file_name,
                                                      performer='')]
                           ))
    client.disconnect()
    return 0

if __name__ == '__main__':
    import sys
    try:
        main(sys.argv[0:])
    except sqlite3.OperationalError:
        for x in range(4, 1):
            sys.argv[7] = x
            try:
                main(sys.argv[0:])
                break
            except sqlite3.OperationalError:
                continue