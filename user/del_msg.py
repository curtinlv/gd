import time

from telethon import events

# from .login import user
from .. import user

@user.on(events.NewMessage(pattern=r'^del[ 0-9]*$', outgoing=True))
async def del_msg(event):
    try:
        num = event.raw_text.split(' ')
        if isinstance(num, list) and len(num) == 2:
            count = int(num[-1])
        else:
            count = 10
        await event.delete()
        count_buffer = 0
        async for message in user.iter_messages(event.chat_id, from_user="me"):
            if count_buffer == count:
                break
            await message.delete()
            count_buffer += 1
        notification = await user.send_message(event.chat_id, f'已删除{count_buffer}/{count}')
        time.sleep(.5)
        await notification.delete()
    except Exception as e:
        await user.send_message(event.chat_id, str(e))
