from pyrogram import Client, filters, enums
from pyshorteners import Shortener
from shortzy import Shortzy
from info import info
from database.utils import progress_for_pyrogram, convert, humanbytes
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.errors import FloodWait, UserNotParticipant
import os 
import humanize
from stream.utils.human_readable import humanbytes
from urllib.parse import quote_plus
from stream.utils.file_properties import get_name, get_hash, get_media_file_size
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

async def get_channel_shortlink(link):
    url = 'https://tnshort.net/api'
    params = {'api': "d03a53149bf186ac74d58ff80d916f7a79ae5745", 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            return data["shortenedUrl"]

async def get_channel_shortlinkk(url):
    if True:
        shortzy = Shortzy(URL_SHORTNER_WEBSITE_API, URL_SHORTENR_WEBSITE)
        try:
            url = await shortzy.convert(url)
        except Exception as e:
            url = await shortzy.get_quick_link(url)

    return url

@Client.on_message(filters.channel & (filters.document | filters.video)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
#        user_id = message.from_user.id
#        username =  message.from_user.mention
        channel_name = broadcast.chat.title
        channel_id = broadcast.chat.id
        log_msg = await broadcast.forward(
            chat_id=LOG_CHANNEL,
        )
        fileName = get_name(log_msg)
        filesize = humanbytes(get_media_file_size(log_msg))
        star_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        star_download = f"{URL}download/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        shortened_link = await get_channel_shortlinkk(star_stream)
        await log_msg.reply_text(
            text=f"**Link Generated Successfully\nFile Name :- {fileName} \n\nFile Size :- {filesize}\n\nChannel Name :- `{channel_name}`\n\nChannel ID :-** `{channel_id}`",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=star_download),  # we download Link
                                                InlineKeyboardButton('▶Stream online', url=star_stream)]])  # web stream Link
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Fast Download Link", url=shortened_link)]])  # web stream Link
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=FILES_CHANNEL,
                             text=f"Got Floodwait Of {str(w.x)}s FROM {broadcast.chat.title}\n\n**CHANNEL ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=FILES_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Can't Edit Boardcast Message!\nError:  **Give me edit permission in updates and bin Channel!{e}**")
