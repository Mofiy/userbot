import logging

import uvloop
from pyrogram import enums
from configparser import ConfigParser
from pyrogram import Client
from database import BotDatabase

__version__ = 0.0002

config = ConfigParser()
config.read(filenames='config.ini')

API_ID = config.get('pyrogram', 'api_id')
API_HASH = config.get('pyrogram', 'api_hash')

bot = Client(name='my_account', api_id=API_ID, api_hash=API_HASH)


@bot.on_message()
async def get_message(client, message):
    if message.from_user.id not in [467907567, 1240917788]:
        return
    chat = message.text.strip()
    print("my id : ", bot.me.id)
    print(f"BOT receive text message : {chat}")
    if chat[0] == '-' or chat.isdigit():
        print("change to int : ", chat)
        chat = int(chat)
    try:
        chat_data = await bot.get_chat(chat_id=chat)
    except Exception:
        await message.reply(f"this is not group or channel name")
    else:
        # print("after get_chat :\n", chat_data)
        await message.reply(f"chat_info :\n "
                            f"ID: {chat_data.id}\n"
                            f"TYPE {chat_data.type}\n"
                            f"TITLE: {chat_data.title}\n"
                            f"USERNAME: {chat_data.username}\n")
        print(chat_data.type)
        if str(chat_data.type) == 'ChatType.CHANNEL':
            i = 0
            j = 0
            async for l in bot.get_chat_history(chat_id=chat_data.linked_chat.id, limit=10000):
                if l.sender_chat != None:
                    continue
                print(f"{i}\t{l.from_user.id}"
                      f"\t{l.from_user.username}"
                      f"\t{l.from_user.first_name}"
                      f"\t{l.from_user.status}"
                      f"\t{l.from_user.last_online_date}")
                if str(l.from_user.status) in ['UserStatus.ONLINE', 'UserStatus.RECENTLY', 'UserStatus.LAST_WEEK'] and \
                        not l.from_user.is_bot and \
                        not l.from_user.is_fake and \
                        not l.from_user.is_scam and \
                        not l.from_user.is_restricted and \
                        not l.from_user.is_support and \
                        not l.from_user.is_deleted:      # Check user that still alive and was online not long time ago
                    user = {"user_id": l.from_user.id,
                      "first_name": l.from_user.first_name,
                      "username": l.from_user.username,
                      "chat_id": chat_data.id}
                    if database.get_user(l.from_user.id) == None:
                        database.save_user(user)
                        j = j + 1
                    else:
                        database.update_user(user)
                pass
                i = i + 1
            await message.reply(f"{i} users found in this group\n"
                                f"{j} users was saved")
            print(f"{i} users found in this group"
                  f"{j} users was saved")
        elif str(chat_data.type) == 'ChatType.SUPERGROUP':
            bot.join_chat(chat_id=chat_data.id)
            i = 0
            j = 0
            async for l in bot.get_chat_members(chat_id=chat_data.id):
                print(f"{i}\t{l.user.id}"
                      f"\t{l.user.username}"
                      f"\t{l.user.first_name}"
                      f"\t{l.user.status}"
                      f"\t{l.user.last_online_date}")
                if str(l.user.status) in ['UserStatus.ONLINE', 'UserStatus.RECENTLY', 'UserStatus.LAST_WEEK'] and \
                        not l.user.is_bot and \
                        not l.user.is_fake and \
                        not l.user.is_scam and \
                        not l.user.is_restricted and \
                        not l.user.is_support and \
                        not l.user.is_deleted:  # Check user that still alive and was online not long time ago
                    user = {"user_id": l.user.id,
                            "first_name": l.user.first_name,
                            "username": l.user.username,
                            "chat_id": chat_data.id}
                    if database.get_user(l.user.id) == None:
                        database.save_user(user)
                    else:
                        database.update_user(user)
                    j = j + 1
                pass
                i = i + 1
            await message.reply(f"{i} users found in this group\n"
                                f"{j} users was saved")
            print(f"{i} users found in this group"
                  f"{j} users was saved")
        print("end")




if __name__ == "__main__":
    database = BotDatabase("database.db")
    bot.run()

