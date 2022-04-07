#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from telethon import events

from .. import chat_id, jdbot, logger, ch_name, BOT_SET


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/cx$'))
async def cxjc(event):
    try:        
        cmd = "ps -ef"
        f = os.popen(cmd)
        txt = f.readlines() 
        strReturn=""
        intcount=0
        if txt:
            for line in txt:
                if "timeout" in line:
                    continue
                if "/ql/build" in line:
                    continue
                if "backend" in line:
                    continue
                if "node" in line and ".js" in line :
                    pid = line.split()[0].ljust(10,' ')
                    pid_name = line.split()[4]
                    res ="/kill"+pid+'文件名: '+pid_name+'\n'
                    strReturn=strReturn+res
                    intcount=intcount+1
                if "python3" in line and ".py" in line:
                    pid = line.split()[0].ljust(10,' ')
                    pid_name = line.split()[4]
                    res ="/kill"+pid+'文件名: '+pid_name+'\n'
                    strReturn=strReturn+res
                    intcount=intcount+1
                if intcount==35:
                    intcount=0
                    if strReturn:
                        await jdbot.send_message(chat_id, strReturn)
                    strReturn=""
            if strReturn:
                await jdbot.send_message(chat_id, strReturn)
            else:
                await jdbot.send_message(chat_id,'当前系统未执行任何脚本')
        else:
            await jdbot.delete_messages(chat_id,msg)
            await jdbot.send_message(chat_id,'当前系统未执行任何脚本')
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(cxjc, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

