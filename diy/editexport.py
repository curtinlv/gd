#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
import re
import sys
from asyncio import exceptions

from telethon import events, Button

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import press_event, V4, QL, split_list, row
from ..diy.utils import read, write


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/export$'))
async def mychangeexport(event):
    try:
        SENDER = event.sender_id
        configs = read("list")
        knames, vnames, notes, btns = [], [], [], []
        if V4:
            for config in configs:
                if "第五区域" in config and "↓" in config:
                    start_line = configs.index(config) + 1
                elif "第五区域" in config and "↑" in config:
                    end_line = configs.index(config)
                    break
            for config in configs[start_line:end_line]:
                if "export" in config and "##" not in config:
                    kv = config.replace("export ", "")
                    kname = kv.split("=")[0]
                    try:
                        vname = re.findall(r"[^\"']+(?=\"|')", kv)[1]
                    except:
                        vname = '你没有设置任何值'
                    if " # " in kv:
                        note = re.findall(r"(?<=#\s).*", kv)[0]
                    else:
                        note = 'none'
                    knames.append(kname), vnames.append(vname), notes.append(note)
                elif "↓" in config:
                    break
        elif QL:
            for config in configs:
                if "## 其他需要的变量" in config:
                    line = configs.index(config)
                    break
            for config in configs[line:]:
                if "export" in config:
                    kv = config.replace("export ", "")
                    kname = kv.split("=")[0]
                    try:
                        vname = re.findall(r"[^\"']+(?=\"|')", kv)[1]
                    except:
                        vname = '你没有设置任何值'
                    if " # " in kv:
                        note = re.findall(r"(?<=#\s).*", kv)[0]
                    else:
                        note = 'none'
                    knames.append(kname), vnames.append(vname), notes.append(note)
        for i in range(len(knames)):
            if notes[i] != 'none':
                btn = Button.inline(notes[i], data=knames[i])
            else:
                btn = Button.inline(knames[i], data=knames[i])
            btns.append(btn)
        btns.append(Button.inline("取消对话", data='cancel'))
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await jdbot.send_message(chat_id, "这是查询到的环境变量名称\n请问需要查看哪一个？", buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            valuedata = vnames[knames.index(res)]
            keydata = knames[knames.index(res)]
            btns = [
                Button.inline("修改变量", data="change"),
                Button.inline("删除变量", data="delete"),
                Button.inline("取消对话", data='cancel')
            ]
            msg = await jdbot.edit_message(msg, f"这是{res}变量，对应的值为：\n```{valuedata}```\n请做出您的选择：", buttons=split_list(btns, row))
            kname = res
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            elif res == "change":
                loop = True
                await jdbot.delete_messages(chat_id, msg)
                btns.append(Button.inline("取消对话", data="cancel"))
                while loop:
                    valuedatamsg = await jdbot.send_message(chat_id, f"```{valuedata}```")
                    msg = await conv.send_message("上一条消息为待修改的值\n现在请回复你所需要设置的新值")
                    vname = await conv.get_response()
                    vname = vname.raw_text
                    btns_yn = [Button.inline("是", data="yes"), Button.inline("否", data="no")]
                    msg = await jdbot.edit_message(msg, f'好的，请稍等\n键名：{kname}\n值名：{vname}\n请问是这样吗？', buttons=split_list(btns_yn, row))
                    convdata = await conv.wait_event(press_event(SENDER))
                    res = bytes.decode(convdata.data)
                    if res == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                        conv.cancel()
                        return
                    elif res == 'no':
                        await jdbot.delete_messages(chat_id, valuedatamsg)
                        await jdbot.delete_messages(chat_id, msg)
                    else:
                        await jdbot.delete_messages(chat_id, valuedatamsg)
                        msg = await jdbot.edit_message(msg, f'好的，请稍等\n你设置变量为：{kname}="{vname}"')
                        loop = False
                        conv.cancel()
                configs = read("str")
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', f'{kname}="{vname}"', configs)
                write(configs)
                await asyncio.sleep(1.5)
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, "修改环境变量成功")
            elif res == "delete":
                btns_yn = [Button.inline("是", data=res), Button.inline("否", data="no")]
                msg = await jdbot.edit_message(msg, f"这是{keydata}变量，对应的值为：\n```{valuedata}```\n请问你确定要删除此变量吗？", buttons=split_list(btns_yn, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res1 = bytes.decode(convdata.data)
                if res1 == 'no':
                    await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                configs = read("str")
                configs = re.sub(f'(?:^|\n?)export {keydata}=[\'|\"].*[\'|\"].*\n?', "\n", configs)
                write(configs)
                await asyncio.sleep(0.5)
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, "删除环境变量成功")
                conv.cancel()
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
    jdbot.add_event_handler(mychangeexport, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))