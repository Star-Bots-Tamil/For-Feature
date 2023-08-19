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

@Client.on_callback_query(
    filters.create(lambda _, __, query: query.data.startswith("webmi"))
)
async def __(c, m):
    # https://github.com/eyaadh/megadlbot_oss/blob/306fb21dbdbdc8dc17294a6cb7b7cdafb11e44da/mega/helpers/media_info.py#L30
    try:
        await m.answer()
    except Exception:
        pass

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_name = os.path.join(temp_dir, "StarMoviesBot.log")
        log = await m.message.download(temp_file_name)
        neko_endpoint = "https://nekobin.com/api/documents"
        async with aiohttp.ClientSession() as nekoSession:
            payload = {"content": open(log, "r").read()}
            async with nekoSession.post(neko_endpoint, data=payload) as resp:
                resp = await resp.file()
                neko_link = f"https://nekobin.com/{resp['result']['key']}"
        logger.debug(neko_link)
        await m.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Web URL", url=neko_link)]])
)

def throwbin(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = {'id': 'null', 'paste': x, 'title': asciigen(10)}
    response = requests.put("https://api.throwbin.io/v1/store", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://throwbin.io/{}".format(jsoncont["id"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://throwbin.io/{}".format(jsoncont["id"])+"\n")

def pastr(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = {'destruct': "none", 'paste': x, 'syntax': "nohighlight", 'title': asciigen(10)}
    response = requests.post("https://pastr.io/api/create", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://pastr.io/{}".format(jsoncont["data"]["url"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://pastr.io/{}".format(jsoncont["data"]["url"])+"\n")

def hastebin(x, proxy):
    headers = { 'Content-Type': 'application/json;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    payload = str(x)
    response = requests.post("https://hastebin.com/documents", headers=headers,json=payload,proxies={"http": proxy, "https": proxy},timeout=20)
    jsoncont = json.loads(response.content)
    print("https://hastebin.com/{}".format(jsoncont["key"]))
    with open ("pasted.txt","a+") as handle:
        handle.write("https://hastebin.com/{}".format(jsoncont["key"])+"\n")
        
