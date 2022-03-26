#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from asyncio import exceptions

import os
import re
import requests
import sys
import time
from telethon import events, Button

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import press_event, V4, QL, cmd, split_list, row, AUTH_FILE, cron_manage_QL
from ..diy.utils import ql_token, read, write


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://github\.com/\S+git$'))
async def myaddrepo(event):
    try:
        SENDER = event.sender_id
        url = event.raw_text
        short_url, git_name = url.split('/')[-1].replace(".git", ""), url.split("/")[-2]
        if V4:
            tips_1 = [
                f'正在设置 OwnRepoBranch（分支） 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支',
                '正在设置 OwnRepoPath（路径） 的值\n该值为你要使用的脚本在分支的哪个路径'
            ]
            tips_2 = [
                f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
                f'回复 scripts/jd normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts/jd 和 normal文件夹下\n回复 root cron 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 根目录 和 cron 文件夹下\n具体目录路径以你所发仓库实际为准\n'
            ]
            tips_3 = [
                [
                    Button.inline('"默认" 分支', data='root'),
                    Button.inline('"main" 分支', data='main'),
                    Button.inline('"master" 分支', data='master'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline('仓库根目录', data='root'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ]
            ]
        else:
            tips_1 = [
                f'正在设置 branch（分支） 的值\n该值为你想使用脚本在[仓库]({url})的哪个分支',
                f'正在设置 path（路径） 的值\n该值为你要使用的脚本在分支的哪个路径\n或你要使用根目录下哪些名字开头的脚本（可用空格或|隔开）',
                f'正在设置 blacklist（黑名单） 的值\n该值为你不需要使用以哪些名字开头的脚本（可用空格或|隔开）',
                f'正在设置 dependence（依赖文件） 的值\n该值为你想使用的依赖文件名称',
                f'正在设置定时拉取仓库的 cron 表达式，可默认每日 0 点'
            ]
            tips_2 = [
                f'回复 main 代表使用 [{short_url}]({url}) 仓库的 "main" 分支\n回复 master 代表使用 [{short_url}]({url}) 仓库的 "master" 分支\n具体分支名称以你所发仓库实际为准\n',
                f'回复 scripts normal 代表你想使用的脚本在 [{short_url}]({url}) 仓库的 scripts 和 normal文件夹下\n具体目录路径以你所发仓库实际为准\n',
                f'回复 jd_ jx_ 代表你不想使用开头为 jd_ 和 jx_ 的脚本\n具体文件名以你所发仓库实际、以你个人所需为准\n',
                f'回复你所需要安装依赖的文件全称\n具体文件名以你所发仓库实际、以你个人所需为准\n',
                f"回复你所需设置的 cron 表达式"
            ]
            tips_3 = [
                [
                    Button.inline('"默认" 分支', data='root'),
                    Button.inline('"main" 分支', data='main'),
                    Button.inline('"master" 分支', data='master'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline('仓库根目录', data='root'),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("不设置", data="root"),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("不设置", data="root"),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ],
                [
                    Button.inline("默认每天0点", data="root"),
                    Button.inline('手动输入', data='input'),
                    Button.inline('取消对话', data='cancel')
                ]
            ]
        replies = []
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            for tip_1 in tips_1:
                i = tips_1.index(tip_1)
                msg = await conv.send_message(tip_1, buttons=split_list(tips_3[i], row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'input':
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await conv.send_message(tips_2[i])
                    reply = await conv.get_response()
                    res = reply.raw_text
                replies.append(res)
                await jdbot.delete_messages(chat_id, msg)
            conv.cancel()
        if V4:
            nums = []
            configs = read("list")
            for config in configs:
                if '启用其他开发者的仓库方式一' in config:
                    start_line = configs.index(config)
                elif 'OwnRepoUrl1=""' in config and '##' in config:
                    nums = [1]
                    break
                elif 'OwnRepoUrl2=""' in config and '##' in config:
                    nums = [2]
                    break
                elif 'OwnRepoUrl=""' in config and '##' in config:
                    num = int(re.findall(r'(?<=OwnRepoUrl)[\d]+(?==")', config)[0])
                    nums.append(num)
                elif '启用其他开发者的仓库方式二' in config:
                    end_line = configs.index(config)
                    break
            if len(nums) == 0:
                nums = [0]
            nums.sort()
            OwnRepoUrl = f'OwnRepoUrl{nums[-1] + 1}="{url}"\n'
            OwnRepoBranch = f'OwnRepoBranch{nums[-1] + 1}="{replies[0].replace("root", "")}"\n'
            Path = replies[1].replace("root", "''")
            if Path == "''":
                OwnRepoPath = f'OwnRepoPath{nums[-1] + 1}=""\n'
            else:
                OwnRepoPath = f'OwnRepoPath{nums[-1] + 1}="{Path}"\n'
            if nums[-1] == 0:
                insert = f'{OwnRepoUrl}{OwnRepoBranch}{OwnRepoPath}'
                configs.insert(configs[end_line] - 1, insert)
            else:
                for config in configs[start_line:end_line]:
                    if config.find(f'OwnRepoUrl{nums[-1]}') != -1 and config.find("## ") == -1:
                        configs.insert(configs.index(config) + 1, OwnRepoUrl)
                    elif config.find(f'OwnRepoBranch{nums[-1]}') != -1 and config.find("## ") == -1:
                        configs.insert(configs.index(config) + 1, OwnRepoBranch)
                    elif config.find(f'OwnRepoPath{nums[-1]}') != -1 and config.find("## ") == -1:
                        configs.insert(configs.index(config) + 1, OwnRepoPath)
            write(configs)
            await jdbot.send_message(chat_id, "现在开始拉取仓库，稍后请自行查看结果")
            await cmd("jup own")
        else:
            branch = replies[0].replace("root", "")
            path = replies[1].replace(" ", "|").replace("root", "")
            blacklist = replies[2].replace(" ", "|").replace("root", "")
            dependence = replies[3].replace("root", "")
            cron = replies[4].replace("root", "0 0 * * *")
            command = f'ql repo {url} "{path}" "{blacklist}" "{dependence}" "{branch}"'
            data = {
                "name": "拉取仓库",
                "command": command,
                "schedule": cron
            }
            res = cron_manage_QL("add", data, ql_token(AUTH_FILE))
            if res['code'] == 200:
                await jdbot.send_message(chat_id, "新增仓库的定时任务成功")
                await cmd(command)
            elif res['code'] == 500:
                await jdbot.send_message(chat_id, "cron表达式有错误！")
            else:
                await jdbot.send_message(chat_id, "发生未知错误，无法新增仓库")
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
    jdbot.add_event_handler(myaddrepo, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^ql repo'))
async def myqladdrepo(event):
    try:
        if QL:
            SENDER = event.sender_id
            message = event.message.text
            repo = message.replace("ql repo", "")
            if len(repo) <= 1:
                await jdbot.send_message(chat_id, "没有设置仓库链接")
                return
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("请设置任务名称")
                reply = await conv.get_response()
                taskname = reply.raw_text
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message("请设置 cron 表达式")
                reply = await conv.get_response()
                cron = reply.raw_text
                await jdbot.delete_messages(chat_id, msg)
                conv.cancel()
            data = {
                "command": message.replace('"', '\"'),
                "name": taskname,
                "schedule": cron
            }
            res = cron_manage_QL("add", data, ql_token(AUTH_FILE))
            if res['code'] == 200:
                await jdbot.send_message(chat_id, "新增仓库的定时任务成功")
                await cmd(message)
            elif res['code'] == 500:
                await jdbot.send_message(chat_id, "cron表达式有错误！")
            else:
                await jdbot.send_message(chat_id, "发生未知错误，无法新增仓库")
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(myqladdrepo, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/repo$'))
async def myrepo(event):
    try:
        SENDER = event.sender_id
        if V4:
            btns = [
                Button.inline("启动", data="start"),
                Button.inline("停止", data="stop"),
                Button.inline("删除", data="delete"),
                Button.inline("取消会话", data="cancel")
            ]
        else:
            btns = [
                Button.inline("启用", data="enable"),
                Button.inline("禁用", data="disable"),
                Button.inline("删除", data="delete"),
                Button.inline("更新仓库", data="run"),
                Button.inline("取消会话", data="cancel")
            ]
        if V4:
            configs = read("list")
            r_names, r_urls, r_namesline, r_branchs, r_branchsline, r_paths, r_pathsline, r_status, r_nums, btns_1 = [], [], [], [], [], [], [], [], [], []
            for config in configs:
                if config.find("OwnRepoUrl") != -1 and config.find("## ") == -1:
                    url = config.split("=")[-1].replace('"', "")
                    r_urls.append(url)
                    reponum = re.findall(r"\d", config.split("=")[0])[0]
                    r_nums.append(reponum)
                    r_names.append(url.split("/")[-2])
                    r_namesline.append(configs.index(config))
                    if config.find("#") != -1:
                        status = "禁用"
                    else:
                        status = "启用"
                    r_status.append(status)
                elif config.find("OwnRepoBranch") != -1 and config.find("## ") == -1:
                    branch = config.split("=")[-1].replace('"', "")
                    if branch == '':
                        branch = "None"
                    r_branchs.append(branch)
                    r_branchsline.append(configs.index(config))
                elif config.find("OwnRepoPath") != -1 and config.find("## ") == -1:
                    path = config.split("=")[-1].replace('"', "")
                    if path == '':
                        path = "None"
                    r_paths.append(path)
                    r_pathsline.append(configs.index(config))
                elif config.find("启用其他开发者的仓库方式二") != -1:
                    break
            for r_name in r_names:
                btns_1.append(Button.inline(r_name, data=r_name))
            btns_1.append(Button.inline("更新全部仓库", data="jup own"))
            btns_1.append(Button.inline("取消会话", data="cancel"))
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("这是你目前添加的仓库", buttons=split_list(btns_1, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'jup own':
                    msg = await jdbot.edit_message(msg, '准备拉取全部仓库')
                    os.system(res)
                    conv.cancel()
                    return
                i = r_names.index(res)
                name, url, branch, path, status, num = r_names[i], r_urls[i], r_branchs[i], r_paths[i], r_status[i], \
                                                       r_nums[i]
                nameline, branchline, pathline = r_namesline[i], r_branchsline[i], r_pathsline[i]
                data = f'仓库名：{name}\n仓库链接：{url}仓库分支：{branch}文件路径：{path}状态：{status}\n'
                msg = await jdbot.edit_message(msg, f'{data}请做出你的选择', buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'start':
                    await jdbot.edit_message(msg, "启动仓库")
                    configs[nameline] = configs[nameline].replace("# ", "")
                    configs[branchline] = configs[branchline].replace("# ", "")
                    configs[pathline] = configs[pathline].replace("# ", "")
                    configs = ''.join(configs)
                elif res == 'stop':
                    await jdbot.edit_message(msg, "停止仓库")
                    configs[nameline] = f"# {configs[nameline]}"
                    configs[branchline] = f"# {configs[branchline]}"
                    configs[pathline] = f"# {configs[pathline]}"
                    configs = ''.join(configs)
                elif res == 'delete':
                    await jdbot.edit_message(msg, "删除仓库")
                    configs = read("str")
                    configs = re.sub(f"OwnRepoUrl{num}=.*", "", configs)
                    configs = re.sub(f"OwnRepoBranch{num}=.*", "", configs)
                    configs = re.sub(f"OwnRepoPath{num}=.*", "", configs)
                write(configs)
        else:
            token = ql_token(AUTH_FILE)
            url = 'http://127.0.0.1:5600/api/crons'
            body = {
                "searchValue": "ql repo",
                "t": int(round(time.time() * 1000))
            }
            headers = {'Authorization': f'Bearer {token}'}
            resp = requests.get(url, params=body, headers=headers).json()['data']
            datas, btns_1 = [], []
            for data in resp:
                name = data['name']
                command = data['command']
                schedule = data['schedule']
                status = '启用'
                try:
                    _id = data['_id']
                except KeyError:
                    _id = data['id']
                if data['status'] == 1:
                    status = '禁用'
                datas.append([name, command, schedule, status, _id])
            for _ in datas:
                i = datas.index(_)
                btns_1.append(Button.inline(_[0], data=f"{str(i)}"))
            btns_1.append(Button.inline("取消会话", data="cancel"))
            async with jdbot.conversation(SENDER, timeout=60) as conv:
                msg = await conv.send_message("这是你目前添加的仓库", buttons=split_list(btns_1, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                data = datas[int(res)]
                info = f"任务名：{data[0]}\n命令：{data[1]}\n定时：{data[2]}\n状态：{data[3]}\n"
                msg = await jdbot.edit_message(msg, f"{info}请做出你的选择", buttons=split_list(btns, row))
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                _id = [data[4]]
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == 'delete':
                    r = requests.delete(f"{url}?t={str(round(time.time() * 1000))}", json=_id, headers=headers).json()
                else:
                    r = requests.put(f'{url}/{res}?t={str(round(time.time() * 1000))}', json=_id,
                                     headers=headers).json()
                conv.cancel()
            if r['code'] == 200:
                await jdbot.edit_message(msg, "操作成功")
            else:
                await jdbot.edit_message(msg, "操作失败，请手动尝试")
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
    jdbot.add_event_handler(myqladdrepo, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))
