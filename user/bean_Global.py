from PIL import Image, ImageFont, ImageDraw
from telethon import events
from .. import LOG_DIR,BOT_DIR,user
from prettytable import PrettyTable
import subprocess
from ..bot.beandata import get_bean_data
from ..bot.utils import V4
from uuid import uuid4


BEAN_IN_FILE = f'{LOG_DIR}/bean_income-{uuid4()}.csv'
BEAN_OUT_FILE = f'{LOG_DIR}/bean_outlay-{uuid4()}.csv'
BEAN_TOTAL_FILE = f'{LOG_DIR}/bean_total-{uuid4()}.csv'
BEAN_IMG = f'{LOG_DIR}/bean-{uuid4()}.jpg'
FONT_FILE = f'{BOT_DIR}/font/jet.ttf'


@user.on(events.NewMessage(pattern=r'^bb', outgoing=True))
async def bot_bean(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: bb 1 或 bb ptpin')
        return    
    else:
        await event.edit('开始查询账号'+text+'的资产，请稍后...')
    
    if V4 and text == 'in':
        subprocess.check_output(
            'jcsv', shell=True, stderr=subprocess.STDOUT)
        creat_bean_counts(BEAN_IN_FILE)
        await event.delete()
        await user.send_message(event.chat_id, '您的近日收入情况', file=BEAN_IMG)
        
    elif V4 and text == 'out':
        subprocess.check_output(
            'jcsv', shell=True, stderr=subprocess.STDOUT)
        creat_bean_counts(BEAN_OUT_FILE)
        await event.delete()
        await user.send_message(event.chat_id, '您的近日支出情况', file=BEAN_IMG)
        
    elif not V4 and (text == 'in' or text == 'out' or text is None):
        await event.delete()
        await user.send_message(event.chat_id,'QL暂不支持使用bean in、out ,请使用/bean n n为数字')
        
    elif text and int(text):
        res = get_bean_data(int(text))
        if res['code'] != 200:
            await event.delete()
            await user.send_message(event.chat_id, f'something wrong,I\'m sorry\n{str(res["data"])}')
        else:
            creat_bean_count(res['data'][3], res['data'][0], res['data'][1], res['data'][2][1:])
            await event.delete()
            await user.send_message(event.chat_id, f'您的账号{text}收支情况', file=BEAN_IMG)
    elif not text:
        subprocess.check_output(
            'jcsv', shell=True, stderr=subprocess.STDOUT)
        creat_bean_counts(BEAN_TOTAL_FILE)
        await event.delete()
        await user.send_message(event.chat_id, '您的总京豆情况', file=BEAN_IMG)
    else:
        await event.delete()
        await user.send_message(event.chat_id, '青龙暂仅支持/bean n n为账号数字') 


def creat_bean_count(date, beansin, beansout, beanstotal):
    tb = PrettyTable()
    tb.add_column('DATE', date)
    tb.add_column('BEANSIN', beansin)
    tb.add_column('BEANSOUT', beansout)
    tb.add_column('TOTAL', beanstotal)
    font = ImageFont.truetype(FONT_FILE, 18)
    im = Image.new("RGB", (500, 260), (244, 244, 244))
    dr = ImageDraw.Draw(im)
    dr.text((10, 5), str(tb), font=font, fill="#000000")
    im.save(BEAN_IMG)


def creat_bean_counts(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    tb = PrettyTable()
    num = len(data[-1].split(',')) - 1
    title = ['DATE']
    for i in range(0, num):
        title.append('COUNT'+str(i+1))
    tb.field_names = title
    data = data[-7:]
    for line in data:
        row = line.split(',')
        if len(row) > len(title):
            row = row[:len(title)]
        elif len(row) < len(title):
            i = len(title) - len(row)
            for _ in range(0, i):
                row.append(str(0))
        tb.add_row(row)
    length = 172 + 100 * num
    im = Image.new("RGB", (length, 400), (244, 244, 244))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_FILE, 18)
    dr.text((10, 5), str(tb), font=font, fill="#000000")
    im.save(BEAN_IMG)
