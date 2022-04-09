#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from telethon import events
from .. import chat_id, jdbot, logger
from ..bot.utils import cmd


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/clean(|\s.*\d{1})$'))
async def clean(event):
    try:
        msg_text = event.raw_text.split(' ')
        dayNum = 7
        if len(msg_text) > 1:
            dayNum = msg_text[1]
            msg = await jdbot.send_message(chat_id, f"清理{dayNum}天前日志...")
        else:
            msg = await jdbot.send_message(chat_id, f"默认清理{dayNum}天前日志。可回复[`/clean n`]， n为天数。")
        await cmd('if [ -d /ql/data ];then QL=/ql/data;else QL=/ql; fi; bash ${QL}/jbot/shell/cleaner.sh %s' % dayNum)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


