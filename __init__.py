from telethon import TelegramClient, connection
import json
import os
import logging
from functools import wraps
JD_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# 兼容青龙新版目录
try:
    qlver = os.environ['QL_BRANCH']
    if qlver >= 'v2.12.0':
        QLMain='/ql/data'
    else:
        QLMain = '/ql'
except:
    QLMain = '/ql'

CONFIG_DIR = f"{JD_DIR}/config"
SCRIPTS_DIR = f"{JD_DIR}/scripts"
DIY_DIR = f"{JD_DIR}/own" if os.environ.get("JD_DIR") else f"{JD_DIR}/scripts"
OWN_DIR=f"{JD_DIR}/scripts"
_DiyScripts = f'{JD_DIR}/diyscripts'
DB_DIR = f"{JD_DIR}/db" if os.environ.get("QL_DIR") else None
BOT_DIR = f"{JD_DIR}/jbot"
LOG_DIR = f"{JD_DIR}/log"

SHORTCUT_FILE = f"{CONFIG_DIR}/shortcut.list"
BOT_LOG_FILE = f"{LOG_DIR}/bot/run.log"
BOT_JSON_FILE = f"{CONFIG_DIR}/bot.json"
QR_IMG_FILE = f"{CONFIG_DIR}/qr.jpg"
BOT_SET_JSON_FILE_USER = f"{CONFIG_DIR}/botset.json"
BOT_SET_JSON_FILE = f"{BOT_DIR}/set.json"

with open(f"{CONFIG_DIR}/jk.json", 'r', encoding='utf-8') as f:
    jk = json.load(f)

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s [%(funcName)s] %(message)s ", 
    level=logging.INFO, 
    filename=BOT_LOG_FILE,
    filemode="w"
)
logger = logging.getLogger(__name__)

if not os.path.exists(f"{LOG_DIR}/bot"):
    os.mkdir(f"{LOG_DIR}/bot")

if os.path.exists(BOT_JSON_FILE):
    with open(BOT_JSON_FILE, "r", encoding="utf-8") as f:
        BOT = json.load(f)
        
if os.path.exists(BOT_SET_JSON_FILE_USER):
    with open(BOT_SET_JSON_FILE_USER, "r", encoding="utf-8") as f:
        BOT_SET = json.load(f)
else:
    with open(BOT_SET_JSON_FILE, "r", encoding="utf-8") as f:
        BOT_SET = json.load(f)
        
if BOT_SET.get("开启别名") and BOT_SET["开启别名"].lower() == "true":
    ch_name = True
else:
    ch_name = False
    
chat_id = int(BOT["user_id"])
TOKEN = BOT["bot_token"]
API_ID = BOT["api_id"]
API_HASH = BOT["api_hash"]
PROXY_START = BOT["proxy"]
START_CMD = BOT["StartCMD"]
PROXY_TYPE = BOT["proxy_type"]
connectionType = connection.ConnectionTcpMTProxyRandomizedIntermediate if PROXY_TYPE == "MTProxy" else connection.ConnectionTcpFull

if BOT.get("proxy_user") and BOT["proxy_user"] != "代理的username,有则填写，无则不用动":
    proxy = {
        "proxy_type": BOT["proxy_type"],
        "addr":  BOT["proxy_add"],
        "port": BOT["proxy_port"],
        "username": BOT["proxy_user"],
        "password": BOT["proxy_password"]
    }
elif PROXY_TYPE == "MTProxy":
    proxy = (BOT["proxy_add"], BOT["proxy_port"], BOT["proxy_secret"])
else:
    proxy = (BOT["proxy_type"], BOT["proxy_add"], BOT["proxy_port"])
    
# 开启tg对话
if PROXY_START and BOT.get("noretry") and BOT["noretry"]:
    jdbot = TelegramClient("bot", API_ID, API_HASH, connection=connectionType, proxy=proxy).start(bot_token=TOKEN)
elif PROXY_START:
    jdbot = TelegramClient("bot", API_ID, API_HASH, connection=connectionType, proxy=proxy).start(bot_token=TOKEN)
elif BOT.get("noretry") and BOT["noretry"]:
    jdbot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=TOKEN)
else:
    jdbot = TelegramClient("bot", API_ID, API_HASH, connection_retries=None).start(bot_token=TOKEN)

# 开启tg对话
if PROXY_START and BOT.get('noretry') and BOT['noretry']:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH, connection=connectionType, proxy=proxy)
elif PROXY_START:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH, connection=connectionType, proxy=proxy,
                          connection_retries=None)
elif BOT.get('noretry') and BOT['noretry']:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH)
else:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH, connection_retries=None)
#解决/user重复对话, user?不回复问题
if BOT_SET['开启user'].lower() == 'true':
    logger.info("开启user监控")
    user = user.start()

# 读取监控配置
def readJKfile(func):
    @wraps(func)
    def getjkfile(*args, **kwargs):
        try:
            with open(f"{CONFIG_DIR}/jk.json", 'r', encoding='utf-8') as f:
                jk = json.load(f)
                return func(jk)
                # return func(*args, **kwargs)
        except:
            return func(*args, **kwargs)
    return getjkfile