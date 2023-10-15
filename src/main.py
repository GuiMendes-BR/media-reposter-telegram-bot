from datetime import datetime
from telethon import TelegramClient, events
import logging

from instagram_bot import InstagramBot

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = '17213748'
api_hash = '7b5a61de7e84830b972cb7a8b4aee333'
bot_token = '6527666633:AAH8qm9a0Fop0o43Ze5Bq1epstX4iWohvMI'
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=[-1001917770130],pattern=".*"))
async def my_event_handler(event):
    if 'https://www.instagram.com/' in event.raw_text:
        url = event.raw_text
        instagram = InstagramBot()
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Downloading reels...')
        instagram.download(url, "testeee.mp4")
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Reels downloaded successfully...')

with client:
    client.run_until_disconnected()