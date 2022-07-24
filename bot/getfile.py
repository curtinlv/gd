from telethon import events, Button
import asyncio
from .. import jdbot, chat_id, SCRIPTS_DIR, CONFIG_DIR, logger
from .utils import press_event, backup_file, add_cron, cmd, DIY_DIR, TASK_CMD, V4, split_list, row


@jdbot.on(events.NewMessage(from_users=chat_id))
async def bot_get_file(event):
    """
    定义文件操作
    """
    try:
        if not event.message.file:
            return
        filename = event.message.file.name
        try:
            if not (
                filename.endswith(".py")
                or filename.endswith(".pyc")
                or filename.endswith(".js")
                or filename.endswith(".sh")
            ):
                return
        except:
            return
        SENDER = event.sender_id
        cmdtext = False
        if V4:
            buttons = [
                Button.inline('放入config', data=CONFIG_DIR),
                Button.inline('仅放入scripts', data=SCRIPTS_DIR),
                Button.inline('仅放入own文件夹', data=DIY_DIR),
                Button.inline('放入scripts并运行', data='node1'),
                Button.inline('放入own并运行', data='node'),
                Button.inline('取消', data='cancel')
            ]
        else:
            buttons = [
                Button.inline('放入config', data=CONFIG_DIR),
                Button.inline('仅放入scripts', data=SCRIPTS_DIR),
                Button.inline('放入scripts并运行', data='node1'),
                Button.inline('取消', data='cancel')
            ]
        async with jdbot.conversation(SENDER, timeout=180) as conversation:
            msg = await conversation.send_message("请选择您要放入的文件夹或操作：\n", buttons=split_list(buttons, row))
            byte = await conversation.wait_event(press_event(SENDER))
            res1 = bytes.decode(byte.data)
            if res1 == "cancel":
                await jdbot.edit_message(msg, "对话已取消")
                conversation.cancel()
                return
            await jdbot.delete_messages(chat_id, msg)
            buttons = [Button.inline('是', data='yes'), Button.inline('否', data='no')]
            msg = await conversation.send_message("是否尝试自动加入定时", buttons=buttons)
            byte = await conversation.wait_event(press_event(SENDER))
            res2 = bytes.decode(byte.data)
            if res2 == "cancel":
                await jdbot.edit_message(msg, "对话已取消")
                conversation.cancel()
                return
            if res1 == "node":
                backup_file(f'{DIY_DIR}/{filename}')
                await jdbot.download_media(event.message, DIY_DIR)
                cmdtext = f'{TASK_CMD} {DIY_DIR}/{filename} now'
                if res2 == 'yes':
                    try:
                        with open(f'{DIY_DIR}/{filename}', 'r', encoding='utf-8') as f:
                            resp = f.read()
                    except:
                        resp = "None"
                    await add_cron(jdbot, conversation, resp, filename, msg, SENDER, buttons, DIY_DIR)
                else:
                    await jdbot.edit_message(msg, '脚本已保存到DIY文件夹，并成功运行')
            elif res1 == "node1":
                backup_file(f'{SCRIPTS_DIR}/{filename}')
                await jdbot.download_media(event.message, SCRIPTS_DIR)
                cmdtext = f'{TASK_CMD} {SCRIPTS_DIR}/{filename} now'
                if res2 == 'yes':
                    try:
                        with open(f'{SCRIPTS_DIR}/{filename}', 'r', encoding='utf-8') as f:
                            resp = f.read()
                    except:
                        resp = "None"
                    await add_cron(jdbot, conversation, resp, filename, msg, SENDER, buttons, SCRIPTS_DIR)
                else:
                    await jdbot.edit_message(msg, '脚本已保存到SCRIPTS文件夹，并成功运行')
            else:
                backup_file(f'{res1}/{filename}')
                await jdbot.download_media(event.message, res1)
                if res2 == 'yes':
                    try:
                        with open(f'{res1}/{filename}', 'r', encoding='utf-8') as f:
                            resp = f.read()
                    except:
                        resp = "None"
                    await add_cron(jdbot, conversation, resp, filename, msg, SENDER, buttons, res1)
                else:
                    await jdbot.edit_message(msg, f'{filename}已保存到{res1}文件夹')
            conversation.cancel()
        if cmdtext:
            await cmd(cmdtext)
    except asyncio.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
