#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import requests
import os
import time
import json
import re

from .. import chat_id, jdbot, CONFIG_DIR
from ..bot.utils import V4, QL, mycron, press_event, AUTH_FILE, cron_manage_QL, add_cron_V4, get_cks, CONFIG_SH_FILE

with open(f"{CONFIG_DIR}/diybotset.json", 'r', encoding='utf-8') as f:
    diybotset = json.load(f)
# with open(f"{CONFIG_DIR}/jk.json", 'r', encoding='utf-8') as f:
#     jk = json.load(f)

my_chat_id = int(diybotset['my_chat_id'])


def myids(values, test_id):
    if "," in values:
        ids = values.replace(" ", "").split(",")
        ids = list(map(int, ['%s' % int(_) for _ in ids]))
    else:
        ids = [int(values)]
    ids.append(int(test_id))
    return ids


myzdjr_chatIds = myids(diybotset['myzdjr_chatId'], my_chat_id)

shoptokenIds = myids(diybotset['shoptokenId'], my_chat_id)


QL8, QL2 = False, False
if os.path.exists('/ql/config/env.sh'):
    QL8 = True
else:
    QL2 = True


def ql_token(file):
    with open(file, 'r', encoding='utf-8') as f:
        auth = json.load(f)
    return auth['token']


def checkCookie1():
    expired = []
    cookies = get_cks(CONFIG_SH_FILE)
    for cookie in cookies:
        cknum = cookies.index(cookie) + 1
        if checkCookie2(cookie):
            expired.append(cknum)
    return expired, cookies


def checkCookie2(cookie):
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = requests.get(url, headers=headers).json()
        if r['retcode'] == '1001':
            return True
        else:
            return False
    except:
        return False


# 读取config.sh
def read(arg):
    if arg == "str":
        with open(f"{CONFIG_DIR}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        return configs
    elif arg == "list":
        with open(f"{CONFIG_DIR}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        return configs


# 写入config.sh
def write(configs):
    if isinstance(configs, str):
        with open(f"{CONFIG_DIR}/config.sh", 'w', encoding='utf-8') as f1:
            f1.write(configs)
    elif isinstance(configs, list):
        with open(f"{CONFIG_DIR}/config.sh", 'w', encoding='utf-8') as f1:
            f1.write("".join(configs))


# 读写config.sh
def rwcon(arg):
    if arg == "str":
        with open(f"{CONFIG_DIR}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.read()
        return configs
    elif arg == "list":
        with open(f"{CONFIG_DIR}/config.sh", 'r', encoding='utf-8') as f1:
            configs = f1.readlines()
        return configs
    elif isinstance(arg, str):
        with open(f"{CONFIG_DIR}/config.sh", 'w', encoding='utf-8') as f1:
            f1.write(arg)
    elif isinstance(arg, list):
        with open(f"{CONFIG_DIR}/config.sh", 'w', encoding='utf-8') as f1:
            f1.write("".join(arg))


# 读写wskey.list
def wskey(arg):
    if V4:
        file = f"{CONFIG_DIR}/wskey.list"
    else:
        file = "/ql/db/wskey.list"
    if arg == "str":
        with open(file, 'r', encoding='utf-8') as f1:
            wskey = f1.read()
        return wskey
    elif arg == "list":
        with open(file, 'r', encoding='utf-8') as f1:
            wskey = f1.readlines()
        return wskey
    elif "wskey" in arg and "pin" in arg:
        with open(file, 'w', encoding='utf-8') as f1:
            f1.write(arg)


# # 写入wskey.list
# def write_wskey(wskey):
#     file = f"{CONFIG_DIR}/wskey.list"
#     if not os.path.exists(file):
#         os.system(f"touch {file}")
#     pin = wskey.split(";")[0].split("=")[1]
#     with open(file, 'r', encoding='utf-8') as f1:
#         wskeys = f1.read()
#     if pin in wskeys:
#         wskeys = re.sub(f"pin={pin};wskey=.*;", wskey, wskeys)
#         with open(file, 'w', encoding='utf-8') as f2:
#             f2.write(wskeys)
#     else:
#         with open(file, 'a', encoding='utf-8') as f2:
#             f2.write(wskey + "\n")


# user.py调用
def getbean(i, cookie, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie,
    }
    result, o = '', '-->'
    try:
        res = requests.get(url=url, headers=headers).json()
        if res['code'] == '0':
            followDesc = res['result']['followDesc']
            if followDesc.find('成功') != -1:
                try:
                    for n in range(len(res['result']['alreadyReceivedGifts'])):
                        redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                        rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                        result += f"{o}获得{redWord}{rearWord}"
                except:
                    giftsToast = res['result']['giftsToast'].split(' \n ')[1]
                    result = f"{o}{giftsToast}"
            elif followDesc.find('已经') != -1:
                result = f"{o}{followDesc}"
        else:
            result = f"{o}Cookie 可能已经过期"
    except Exception as e:
        if str(e).find('(char 0)') != -1:
            result = f"{o}无法解析数据包"
        else:
            result = f"{o}访问发生错误：{e}"
    return f"\n账号{str(i).zfill(2)}{result}"


# user.py shoptoken() 调用
async def checkShopToken(tokens, msg):
    # 传入的tokens元素格式 [(1,AAA), (2, BBB)]
    shop = ""
    charts = []
    for token in tokens:
        url = f"https://api.m.jd.com/api?appid=interCenter_shopSign&t={int(time.time() * 1000)}&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body={{%22token%22:%22{token[1]}%22,%22venderId%22:%22%22}}"
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://h5.m.jd.com/",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
        }
        r = requests.post(url, headers=headers).json()
        if r['code'] == 402:
            shop += f"店铺{token[0]}已过期\n"
            msg = await jdbot.edit_message(msg, shop)
            charts.append(f'export MyShopToken{token[0]}="{token[1]}"')
            await asyncio.sleep(0.5)
        else:
            cookies = get_cks(CONFIG_SH_FILE)
            for cookie in cookies:
                venderId = getvenderId(token)
                activityId, endday, actinfo = getActivityInfo(token, venderId)
                dayinfo, day = getsignday(token, venderId, activityId, cookie)
                if int(day) >= int(endday):
                    shop += f"店铺{token[0]}签到已完成\n"
                    msg = await jdbot.edit_message(msg, shop)
                    charts.append(f'export MyShopToken{token[0]}="{token[1]}"')
                await asyncio.sleep(0.5)
        # charts 元素格式 ['export MyShopToken1="AAA"', 'export MyShopToken3="CCC"']
    return charts


def deltoken(charts):
    """
    删除过期店铺
    """
    configs = read("list")
    for chart in charts:
        configs.remove(chart)
    write(configs)
    tokens = re.findall(r'export MyShopToken\d+="(.*)"', read("str"))
    i = 0
    configs = read("list")
    for config in configs:
        if tokens[i] in config:
            line = configs.index(config)
            configs[line] = f'export MyShopToken{i + 1}="{tokens[i]}"'
            i += 1
            if i >= len(tokens):
                break
    write(configs)


def getvenderId(token):
    """
    获取店铺ID
    """
    url = f"https://api.m.jd.com/api?appid=interCenter_shopSign&t={int(time.time() * 1000)}&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body={{%22token%22:%22{token}%22,%22venderId%22:%22%22}}"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://h5.m.jd.com/",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
    }
    res = requests.post(url, headers=headers).json()
    venderId = res['data']['venderId']
    return venderId


def getvenderName(venderId):
    """
    获取店铺名称
    """
    url = f"https://wq.jd.com/mshop/QueryShopMemberInfoJson?venderId={venderId}"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
    }
    res = requests.post(url, headers=headers).json()
    shopName = res['shopName']
    nameinfo = f'\n【店铺】{shopName}\n'
    return shopName, nameinfo


def getActivityInfo(token, venderId):
    """
    获取店铺活动信息
    """
    JD_API_HOST = 'https://api.m.jd.com/api?appid=interCenter_shopSign'
    url = f"{JD_API_HOST}&t={int(time.time() * 1000)}&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body={{%22token%22:%22{token}%22,%22venderId%22:{venderId}}}"
    headers = {
        "accept": "accept",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": f"https://h5.m.jd.com/babelDiy/Zeus/2PAAf74aG3D61qvfKUM5dxUssJQ9/index.html?token={token}&sceneval=2&jxsid=16178634353215523301&cu=true&utm_source=kong&utm_medium=jingfen&utm_campaign=t_2009753434_&utm_term=fa3f8f38c56f44e2b4bfc2f37bce9713",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
    }
    res = requests.post(url, headers=headers).json()
    num = len(res['data']['continuePrizeRuleList'])
    info = ''
    for i in range(num):
        day = res['data']['continuePrizeRuleList'][i]['level']
        discount = res['data']['continuePrizeRuleList'][i]['prizeList'][0]['discount']
        info += f'  └签到{day}天，获得{int(discount)}豆；\n'
    actinfo = f'{info}'
    activityId = res['data']['id']
    endday = res['data']['continuePrizeRuleList'][-1]['level']
    return activityId, endday, actinfo


def getsignday(token, venderId, activityId, cookie):
    """
    获取店铺签到信息
    """
    JD_API_HOST = 'https://api.m.jd.com/api?appid=interCenter_shopSign'
    url = f"{JD_API_HOST}&t={int(time.time() * 1000)}&loginType=2&functionId=interact_center_shopSign_getSignRecord&body={{%22token%22:%22{token}%22,%22venderId%22:{venderId},%22activityId%22:{activityId},%22type%22:56}}"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": cookie,
        "referer": f"https://h5.m.jd.com",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
    }
    res = requests.post(url, headers=headers).json()
    day = res['data']['days']
    dayinfo = f'  └已签到：{day}天。\n'
    return dayinfo, day


def signCollectGift(token, activityId, cookie):
    """
    开始店铺签到
    """
    JD_API_HOST = 'https://api.m.jd.com/api?appid=interCenter_shopSign'
    url = f"{JD_API_HOST}&t={int(time.time() * 1000)}&loginType=2&functionId=interact_center_shopSign_signCollectGift&body={{%22token%22:%22{token}%22,%22venderId%22:688200,%22activityId%22:{activityId},%22type%22:56,%22actionType%22:7}}"
    headers = {
        "accept": "accept",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": cookie,
        "referer": f"https://h5.m.jd.com/babelDiy/Zeus/2PAAf74aG3D61qvfKUM5dxUssJQ9/index.html?token={token}&sceneval=2&jxsid=16178634353215523301&cu=true&utm_source=kong&utm_medium=jingfen&utm_campaign=t_2009753434_&utm_term=fa3f8f38c56f44e2b4bfc2f37bce9713",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/13.5.40"
    }
    res = requests.post(url, headers=headers).json()
    info = res['msg']
    signinfo = f'  └{info}\n'
    return signinfo


# 修改原作者的 cronup() 函数便于我继续进行此功能的编写
async def mycronup(jdbot, conv, resp, filename, msg, SENDER, markup, path):
    try:
        cron = mycron(resp)
        msg = await jdbot.edit_message(msg, f"这是我识别的定时\n```{cron}```\n请问是否需要修改？", buttons=markup)
    except:
        msg = await jdbot.edit_message(msg, f"我无法识别定时，将使用默认定时\n```0 0 * * *```\n请问是否需要修改？", buttons=markup)
    convdata3 = await conv.wait_event(press_event(SENDER))
    res3 = bytes.decode(convdata3.data)
    if res3 == 'confirm':
        await jdbot.delete_messages(chat_id, msg)
        msg = await conv.send_message("请回复你需要设置的 cron 表达式，例如：0 0 * * *")
        cron = await conv.get_response()
        cron = cron.raw_text
        msg = await jdbot.edit_message(msg, f"好的，你将使用这个定时\n```{cron}```")
        await asyncio.sleep(1.5)
    await jdbot.delete_messages(chat_id, msg)
    if QL:
        crondata = {"name": f'{filename.split(".")[0]}', "command": f'task {path}/{filename}', "schedule": f'{cron}'}
        with open(AUTH_FILE, 'r', encoding='utf-8') as f:
            auth = json.load(f)
        cron_manage_QL('add', crondata, auth['token'])
    else:
        add_cron_V4(f'{cron} mtask {path}/{filename}')
    await jdbot.send_message(chat_id, '添加定时任务成功')

# async def upuser(fname, msg):
#     try:
#         furl_startswith = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/"
#         speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
#         msg = await jdbot.edit_message(msg, "开始下载文件")
#         for speed in speeds:
#             resp = requests.get(f"{speed}{furl_startswith}{fname}").text
#             if "#!/usr/bin/env python3" in resp:
#                 break
#         if resp:
#             msg = await jdbot.edit_message(msg, f"下载{fname}成功")
#             path = f"{_JdbotDir}/diy/user.py"
#             backup_file(path)
#             with open(path, 'w+', encoding='utf-8') as f:
#                 f.write(resp)
#         else:
#             await jdbot.edit_message(msg, f"下载{fname}失败，请自行拉取文件进/jbot/diy目录")
#     except Exception as e:
#         await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
#         logger.error('something wrong,I\'m sorry\n' + str(e))
