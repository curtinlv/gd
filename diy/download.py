#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from asyncio import exceptions

import os
import re
import requests
import sys
from telethon import events, Button

from .. import chat_id, jdbot, CONFIG_DIR, SCRIPTS_DIR, OWN_DIR, logger, BOT_DIR, ch_name, BOT
from ..bot.utils import press_event, backup_file, cmd, V4, split_list, row
from ..diy.utils import mycronup, read, write


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://.*(js|py|sh)$'))
async def mydownload(event):
    try:
        SENDER = event.sender_id
        furl = event.raw_text
        if '下载代理' in BOT.keys() and str(BOT['下载代理']).lower() != 'false' and 'github' in furl:
            furl = f'{str(BOT["下载代理"])}/{furl}'
        try:
            resp = requests.get(furl).text
            if "</html>" in resp:
                await jdbot.send_message(chat_id, f"接收到的[链接]({furl})是一个页面并非raw数据，会话结束")
                return
        except Exception as e:
            await jdbot.send_message(chat_id, f"下载失败\n{e}")
            return
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            fname = furl.split('/')[-1]
            fname_cn = ''
            if furl.endswith(".js"):
                fname_cn = re.findall(r"(?<=new\sEnv\(').*(?=')", resp, re.M)
                if fname_cn != []:
                    fname_cn = fname_cn[0]
                else:
                    fname_cn = ''
            if V4:
                btns = [Button.inline('放入config目录', data=CONFIG_DIR), Button.inline('放入jbot/diy目录', data=f'{BOT_DIR}/diy'), Button.inline('放入scripts目录', data=SCRIPTS_DIR), Button.inline('放入own目录', data=OWN_DIR ), Button.inline('取消对话', data='cancel')]
            else:
                btns = [Button.inline('放入config目录', data=CONFIG_DIR), Button.inline('放入scripts目录', data=SCRIPTS_DIR), Button.inline('取消对话', data='cancel')]
            cmdtext = False
            msg = await conv.send_message(f'成功下载{fname_cn}脚本\n现在，请做出你的选择：', buttons=split_list(btns, row))
            convdata = await conv.wait_event(press_event(SENDER))
            res1 = bytes.decode(convdata.data)
            if res1 == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                conv.cancel()
                return
            elif res1 == SCRIPTS_DIR:
                fpath = f"{SCRIPTS_DIR}/{fname}"
                btns = [Button.inline("是", data="confirm"), Button.inline("否", data="cancel")]
                msg = await jdbot.edit_message(msg, f"请问需要运行{fname_cn}脚本吗？", buttons=btns)
                convdata = await conv.wait_event(press_event(SENDER))
                res2 = bytes.decode(convdata.data)
                if res2 == "confirm":
                    cmdtext = f'{cmd} {SCRIPTS_DIR}/{fname} now'
                msg = await jdbot.edit_message(msg, f"请问需要添加定时吗？", buttons=btns)
                convdata = await conv.wait_event(press_event(SENDER))
                res2 = bytes.decode(convdata.data)
                if res2 == 'cancel':
                    await jdbot.edit_message(msg, f"{fname_cn}脚本将保存到{SCRIPTS_DIR}目录")
                else:
                    await mycronup(jdbot, conv, resp, fname, msg, SENDER, btns, SCRIPTS_DIR)
            elif res1 == OWN_DIR:
                fpath = f"{OWN_DIR}/raw/{fname}"
                btns = [Button.inline("是", data="confirm"), Button.inline("否", data="cancel")]
                msg = await jdbot.edit_message(msg, f"请问需要运行{fname_cn}脚本吗？", buttons=btns)
                convdata = await conv.wait_event(press_event(SENDER))
                res2 = bytes.decode(convdata.data)
                if res2 == "confirm":
                    cmdtext = f'{cmd} {fpath} now'
                    await jdbot.edit_message(msg, f"文件将保存到{res1}目录，且已写入配置中，准备执行脚本")
                else:
                    await jdbot.edit_message(msg, f'文件将保存到{res1}目录，且已写入配置中，准备拉取单个脚本，请耐心等待')
                configs = read("list")
                for config in configs:
                    if "OwnRawFile" in config and "##" not in config:
                        line = configs.index(config) + 1
                        configs.insert(line, f"\t{event.raw_text}\n")
                        write(configs)
                        break
                    elif config.find("第五区域") != -1:
                        break
                await cmd("jup own")
            else:
                fpath = f"{res1}/{fname}"
                await jdbot.edit_message(msg, f"文件将保存到{res1}目录")
            backup_file(fpath)
            with open(fpath, 'w+', encoding='utf-8') as f:
                f.write(resp)
            conv.cancel()
        if cmdtext:
            await cmd(cmdtext)
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
    jdbot.add_event_handler(mydownload, events.NewMessage(from_users=chat_id, pattern=BOT['命令别名']['cron']))

