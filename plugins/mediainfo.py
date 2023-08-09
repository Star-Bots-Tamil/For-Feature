import tempfile
import logging
import os
from Script import script
from info import info
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_callback_query(
    filters.create(lambda _, __, query: query.data.startswith("mi"))
)
async def _(c, m):
    try:
        await m.answer()
    except Exception:
        pass

    await m.edit_message_text(
        script.ADDED_TO_QUEUE.format(per_user_process_count=info.MAX_PROCESSES_PER_USER),
    )
    c.process_pool.new_task(
        (
            m.from_user.id,
            ProcessFactory(
                process_type=ProcessTypes.MEDIAINFO, client=c, input_message=m
            ),
        )
    )


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
        temp_file_name = os.path.join(temp_dir, "mediainfo.txt")
        media_info = await m.message.download(temp_file_name)
        neko_endpoint = "https://nekobin.com/api/documents"
        async with aiohttp.ClientSession() as nekoSession:
            payload = {"content": open(media_info, "r").read()}
            async with nekoSession.post(neko_endpoint, data=payload) as resp:
                resp = await resp.json()
                neko_link = f"https://nekobin.com/{resp['result']['key']}"
        logger.debug(neko_link)
        await m.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Web URL", url=neko_link)]])
  )
