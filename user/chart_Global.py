from telethon import events
from .. import LOG_DIR,  user
from ..bot.quickchart import QuickChart
from ..bot.beandata import get_bean_data
from uuid import uuid4

BEAN_IMG = f'{LOG_DIR}/bot/bean-{uuid4()}.jpg'

@user.on(events.NewMessage(pattern=r'^bc', outgoing=True))
async def my_chartinfo(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: bc 1 或 bc ptpin')
        return    
    else:
        await event.edit('开始查询账号'+text+'的资产，请稍后...')
    
    if text and int(text):
        res = get_bean_data(int(text))
        if res['code'] != 200:
            await event.delete()
            await user.send_message(event.chat_id,f'something wrong,I\'m sorry\n{str(res["data"])}')
        else:
            creat_chart(res['data'][3], f'账号{str(text)}',res['data'][0], res['data'][1], res['data'][2][1:])
            await event.delete()
            await user.send_message(event.chat_id, f'您的账号{text}收支情况', file=BEAN_IMG)
    


def creat_chart(xdata, title, bardata, bardata2, linedate):
    qc = QuickChart()
    qc.background_color = '#fff'
    qc.width = "1000"
    qc.height = "600"
    qc.config = {
        "type": "bar",
        "data": {
            "labels": xdata,
            "datasets": [
                {
                    "label": "IN",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata
                },
                {
                    "label": "OUT",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata2
                },
                {
                    "label": "TOTAL",
                    "type": "line",
                    "fill": False,
                    "backgroundColor": "rgb(201, 203, 207)",
                    "yAxisID": "y2",
                    "data": linedate
                }
            ]
        },
        "options": {
            "plugins": {
                "datalabels": {
                    "anchor": 'end',
                    "align": -100,
                    "color": '#666',
                    "font": {
                        "size": 20,
                    }
                },
            },
            "legend": {
                "labels": {
                    "fontSize": 20,
                    "fontStyle": 'bold',
                }
            },
            "title": {
                "display": True,
                "text": f'{title}   收支情况',
                "fontSize": 24,
            },
            "scales": {
                "xAxes": [{
                    "ticks": {
                        "fontSize": 24,
                    }
                }],
                "yAxes": [
                    {
                        "id": "y1",
                        "type": "linear",
                        "display": False,
                        "position": "left",
                        "ticks": {
                            "max": int(int(max([max(bardata), max(bardata2)])+100)*2)
                        },
                        "scaleLabel": {
                            "fontSize": 20,
                            "fontStyle": 'bold',
                        }
                    },
                    {
                        "id": "y2",
                        "type": "linear",
                        "display": False,
                        "ticks": {
                            "min": int(min(linedate)*2-(max(linedate))-100),
                            "max": int(int(max(linedate)))
                        },
                        "position": "right"
                    }
                ]
            }
        }
    }
    qc.to_file(BEAN_IMG)
