from PIL import Image, ImageFont, ImageDraw
from telethon import events, Button
from .. import LOG_DIR, jdbot, chat_id, BOT_SET, BOT_DIR, logger,  ch_name
from prettytable import PrettyTable
import subprocess
from .beandata import get_bean_data
from .utils import V4,split_list, press_event

BEAN_IN_FILE = f'{LOG_DIR}/bean_income.csv'
BEAN_OUT_FILE = f'{LOG_DIR}/bean_outlay.csv'
BEAN_TOTAL_FILE = f'{LOG_DIR}/bean_total.csv'
BEAN_IMG = f'{LOG_DIR}/bean.jpg'
FONT_FILE = f'{BOT_DIR}/font/jet.ttf'


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/bean'))
async def bot_bean(event):
    msg_text = event.raw_text.split(' ')
    try:
        msg = await jdbot.send_message(chat_id, '正在查询，请稍后')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
            
        if text==None:
            SENDER = event.sender_id
            btn = []
            for i in range(11):
                btn.append(Button.inline(str(i+1), data=str(i+1)))
            btn.append(Button.inline('取消', data='cancel'))
            btn = split_list(btn, 3)            
            async with jdbot.conversation(SENDER, timeout=90) as conv:
                info='请选择要查询的账号:'
                msg = await jdbot.edit_message(msg, info, buttons=btn, link_preview=False)
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                else:
                    text = res
                    msg = await jdbot.edit_message(msg, '开始查询账号'+text+'的资产，请稍后...')
        if text==None:
            await jdbot.delete_messages(chat_id, msg)
            return 
            
        if V4 and text == 'in':
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(BEAN_IN_FILE)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的近日收入情况', file=BEAN_IMG)
        elif V4 and text == 'out':
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(BEAN_OUT_FILE)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的近日支出情况', file=BEAN_IMG)
        elif not V4 and (text == 'in' or text == 'out' or text is None):
            await jdbot.edit_message(msg, 'QL暂不支持使用bean in、out ,请使用/bean n n为数字')
        elif text and int(text):
            res = get_bean_data(int(text))
            if res['code'] != 200:
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(res["data"])}')
            else:
                creat_bean_count(res['data'][3], res['data']
                                 [0], res['data'][1], res['data'][2][1:])
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, f'您的账号{text}收支情况', file=BEAN_IMG)
        elif not text:
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(BEAN_TOTAL_FILE)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的总京豆情况', file=BEAN_IMG)
        else:
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '青龙暂仅支持/bean n n为账号数字')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry{str(e)}')

if ch_name:
    jdbot.add_event_handler(bot_bean, events.NewMessage(
        chats=chat_id, pattern=BOT_SET['命令别名']['bean']))


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
