import csv
import re
import json
import asyncio
import configparser
import pandas as pd
from csv import writer
from csv import reader
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

#Config the client

config = configparser.ConfigParser()
config.read("config.ini")


api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = 'https://t.me/thehackernews'

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 1000

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
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

    with open('../data/technews_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)

with client:
    client.loop.run_until_complete(main(phone))



with open('../data/technews_messages.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)
df.to_csv('../data/technews_csvfile.csv', encoding='utf-8', index=False)

f=pd.read_csv("../data/technews_csvfile.csv")
keep_col = ['message']
new_f = f[keep_col]
new_f.to_csv("../data/technews_csvfile.csv", index=False)


with open('../data/technews_csvfile.csv', 'r') as read_obj, \
        open('../data/technews_output.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    for row in csv_reader:
        row.append("technews")
        csv_writer.writerow(row)



with open('../data/technews_output.csv', 'r') as inp, open('../data/technews_first_edit.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] != "" and row[0]!="message":
            new_row = row.copy()
            new_row[0]=''.join(e for e in new_row[0] if ((e.isalnum() or e == " " or e == ".") ) )
            new_row[0] = re.sub("https[^ ]*", " ", new_row[0])
            writer.writerow(new_row)

##########################################################################################################

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = 'https://t.me/sportstarweb'

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 1000

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
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

    with open('../data/sports_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)

with client:
    client.loop.run_until_complete(main(phone))


with open('../data/sports_messages.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)
df.to_csv('../data/sports_csvfile.csv', encoding='utf-8', index=False)

f=pd.read_csv("../data/sports_csvfile.csv")
keep_col = ['message']
new_f = f[keep_col]
new_f.to_csv("../data/sports_csvfile.csv", index=False)

with open('../data/sports_csvfile.csv', 'r') as read_obj2, \
        open('../data/sports_output.csv', 'w', newline='') as write_obj2:
    # Create a csv.reader object from the input file object

    csv_reader2 = csv.reader(read_obj2)
    # Create a csv.writer object from the output file object
    csv_writer2 = csv.writer(write_obj2)
    for row in csv_reader2:
        row.append("sports")
        csv_writer2.writerow(row)

with open('../data/sports_output.csv', 'r') as inp, open('../data/sports_first_edit.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] != "" and row[0]!="message":
            new_row = row.copy()
            new_row[0]=''.join(e for e in new_row[0] if (e.isalnum() or e == " " or e == "."))
            new_row[0] = re.sub("bit.ly[^ ]*", " ", new_row[0])
            new_row[0] = re.sub("https[^ ]*", " ", new_row[0])
            writer.writerow(new_row)




