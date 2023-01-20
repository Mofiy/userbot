import logging
# from flask import Flask

import uvloop
from pyrogram import enums
from configparser import ConfigParser
from pyrogram import Client
from database import BotDatabase

__version__ = 0.0001

config = ConfigParser()
config.read(filenames='config.ini')

API_ID = config.get('pyrogram', 'api_id')
API_HASH = config.get('pyrogram', 'api_hash')

bot = Client(name='my_account', api_id=API_ID, api_hash=API_HASH)
# app = Flask(__name__)

@bot.on_message()
async def get_message(client, message):
    chat = message.text
    print("my id : ", bot.me.id)
    print(f"BOT receive text message : {chat}")
    chat_info = await bot.join_chat(chat_id=chat)
    try:
        chat_data = await bot.get_chat(chat_id=chat)
    except KeyError:
        logging.ERROR(KeyError)
    else:
        await message.reply(f"chat_id :{chat_info.id}")
        # Get members
        i = 0 # users counter
        j = 0 # saved users counter
        async for l in bot.get_chat_members(chat_id=chat_info.id):
            print(f"{i}\t{l.user.id}\t{l.user.username}\t{l.user.first_name}\t{l.user.status}\t{l.user.last_online_date}")
            if l.user.status == 'UserStatus.ONLINE' or \
                    l.user.status == 'UserStatus.RECENTLY' or \
                    l.user.status == 'UserStatus.LAST_WEEK' or \
                    not l.user.is_bot or \
                    not l.user.is_fake or \
                    not l.user.is_scam or \
                    not l.user.is_restricted or \
                    not l.user.is_support or \
                    not l.user.st or \
                    not l.user.is_deleted:      # Check user that still alive and was online not long time ago
                user = {"user_id": l.user.id,
                  "first_name": l.user.first_name,
                  "username": l.user.username,
                  "chat_id": chat_info.id}
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





if __name__ == "__main__":
    database = BotDatabase("database.db")
    bot.run()


# chat_id : -1001648828188
# {
#     "_": "ChatMember",
#     "status": "ChatMemberStatus.ADMINISTRATOR",
#     "user": {
#         "_": "User",
#         "id": 5708442537,
#         "is_self": false,
#         "is_contact": false,
#         "is_mutual_contact": false,
#         "is_deleted": false,
#         "is_bot": true,
#         "is_verified": false,
#         "is_restricted": false,
#         "is_scam": false,
#         "is_fake": false,
#         "is_support": false,
#         "is_premium": false,
#         "first_name": "CHECK BOT",
#         "username": "CHECKBOTROBOT",
#         "dc_id": 2,
#         "photo": {
#             "_": "ChatPhoto",
#             "small_file_id": "AQADAgAD5cAxG0cpkEsAEAIAA6nrP1QBAAM2e9hCBtWm2AAEHgQ",
#             "small_photo_unique_id": "AgAD5cAxG0cpkEs",
#             "big_file_id": "AQADAgAD5cAxG0cpkEsAEAMAA6nrP1QBAAM2e9hCBtWm2AAEHgQ",
#             "big_photo_unique_id": "AgAD5cAxG0cpkEs"
#         }
#     },
#     "joined_date": "2022-11-23 02:05:30",
#     "promoted_by": {
#         "_": "User",
#         "id": 283957495,
#         "is_self": false,
#         "is_contact": false,
#         "is_mutual_contact": false,
#         "is_deleted": false,
#         "is_bot": false,
#         "is_verified": false,
#         "is_restricted": false,
#         "is_scam": false,
#         "is_fake": false,
#         "is_support": false,
#         "is_premium": true,
#         "first_name": "VpsmmOfficial",
#         "status": "UserStatus.RECENTLY",
#         "username": "reklamavpsmm",
#         "emoji_status": {
#             "_": "EmojiStatus",
#             "custom_emoji_id": 5316544190979514276
#         },
#         "dc_id": 2,
#         "photo": {
#             "_": "ChatPhoto",
#             "small_file_id": "AQADAgADtKcxG_fY7BAAEAIAA_fY7BAABFt1qHThsFg2AAQeBA",
#             "small_photo_unique_id": "AgADtKcxG_fY7BA",
#             "big_file_id": "AQADAgADtKcxG_fY7BAAEAMAA_fY7BAABFt1qHThsFg2AAQeBA",
#             "big_photo_unique_id": "AgADtKcxG_fY7BA"
#         }
#     },
#     "can_be_edited": false,
#     "privileges": {
#         "_": "ChatPrivileges",
#         "can_manage_chat": true,
#         "can_delete_messages": true,
#         "can_manage_video_chats": true,
#         "can_restrict_members": true,
#         "can_promote_members": true,
#         "can_change_info": true,
#         "can_post_messages": false,
#         "can_edit_messages": false,
#         "can_invite_users": true,
#         "can_pin_messages": true,
#         "is_anonymous": true
#     }
# }