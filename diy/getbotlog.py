#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from telethon import events

from .. import chat_id, jdbot, logger, LOG_DIR


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/?e$'))
async def getbotlog(event):
    try:
        file = f"{LOG_DIR}/bot/run.log"
        await jdbot.send_message(chat_id, "这是bot的运行日志，用于排查问题所在", file=file)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
