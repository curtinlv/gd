#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import re
import sys

from telethon import events

from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import V4, CONFIG_SH_FILE, get_cks, AUTH_FILE
from ..diy.utils import getbean, my_chat_id

bot_id = int(TOKEN.split(":")[0])
client = user


@client.on(events.NewMessage(chats=[-1001320212725, -1001630980165, my_chat_id]))
async def follow(event):
    try:
        url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), event.message.text)
        if not url:
            return
        i = 0
        info = '关注店铺\n'
        for cookie in get_cks(CONFIG_SH_FILE if V4 else AUTH_FILE):
            i += 1
            info += getbean(i, cookie, url[0])
        await jdbot.send_message(chat_id, info)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
        