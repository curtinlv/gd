#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
import re
import sys
from asyncio import exceptions

from telethon import events, Button

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import press_event, V4
from ..diy.utils import read, write


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'(export\s)?\w*=(".*"|\'.*\')'))
async def myaddexport(event):
    try:
        SENDER = event.sender_id
        messages = event.raw_text.split("\n")
        for message in messages:
            if "export " not in message:
                continue
            kv = message.replace("export ", "")
            kname = kv.split("=")[0]
            vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
            btns = [Button.inline("是", data='yes'), Button.inline("否", data='cancel')]
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message(f"我检测到你需要添加一个环境变量\n键名：{kname}\n值名：{vname}\n请问是这样吗？", buttons=btns)
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                else:
                    msg = await jdbot.edit_message(msg, f"好的，请稍等\n你设置变量为：{kname}=\"{vname}\"")
                conv.cancel()
            configs = read("str")
            await asyncio.sleep(1.5)
            if f"export {kname}=" in configs:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', f'{kname}="{vname}"', configs)
                end = "替换环境变量成功"
            else:
                async with jdbot.conversation(SENDER, timeout=60) as conv:
                    msg = await jdbot.edit_message(msg, f"这个环境变量是新增的，需要给他添加注释嘛？", buttons=btns)
                    convdata = await conv.wait_event(press_event(SENDER))
                    res = bytes.decode(convdata.data)
                    if res == 'cancel':
                        msg = await jdbot.edit_message(msg, "那好吧，准备新增变量")
                        note = ''
                    else:
                        await jdbot.delete_messages(chat_id, msg)
                        msg = await conv.send_message("那请回复你所需要添加的注释")
                        note = await conv.get_response()
                        note = f" # {note.raw_text}"
                    conv.cancel()
                if V4:
                    configs = read("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"{note}\n')
                    configs = ''.join(configs)
                else:
                    configs = read("str")
                    configs += f'\nexport {kname}="{vname}"{note}'
                await asyncio.sleep(1.5)
                end = "新增环境变量成功"
            write(configs)
            await jdbot.edit_message(msg, end)
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")

if ch_name:
    jdbot.add_event_handler(myaddexport, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))