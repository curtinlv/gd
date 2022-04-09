#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from telethon import events
from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/clean$'))
async def clean(event):
    try:
        await cmd('if [ -d /ql/data ];then QL=/ql/data;else QL=/ql; fi; bash ${QL}/jbot/shell/cleaner.sh')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(clean, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

