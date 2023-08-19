import tempfile
import logging
import os
import json
import requests
import string
import random
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

NEKOBIN_URL = "https://nekobin.com/"

@Client.on_callback_query(
    filters.create(lambda _, __, query: query.data.startswith("webmi"))
)
async def __(c, m):
    # https://github.com/eyaadh/megadlbot_oss/blob/306fb21dbdbdc8dc17294a6cb7b7cdafb11e44da/mega/helpers/media_info.py#L30
    try:
        await m.answer()
    except Exception:
        pass
    with open("StarMoviesBot.log", "r") as d_f:
        text = d_f.read()
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            NEKOBIN_URL + "api/documents", json={"content": text}
        ) as resp:
            if resp.status == 201:
                response = await resp.json()
                key = response["result"]["key"]
                file_ext = ".txt"
                final = NEKOBIN_URL + key + file_ext
                final_url = f"{NEKOBIN_URL}{key}{file_ext}"
                final_url_raw = f"{NEKOBIN_URL}raw/{key}{file_ext}"
        await m.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Web URL", url=final_url)]])
)
