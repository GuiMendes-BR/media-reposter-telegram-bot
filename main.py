from datetime import datetime
from telethon import TelegramClient, events

from settings.logger import logger
from settings.config import config

from instagram_bot import InstagramBot

client = TelegramClient('bot', config.telegram_api_id, config.telegram_api_hash).start(
    bot_token=config.telegram_api_bot_token)


@client.on(events.NewMessage(chats=[config.chat_id], pattern=".*"))
async def my_event_handler(event):
    if str(config.instagram_url) in event.raw_text:
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Logging to Instagram...')
        instagram = InstagramBot(
            config.instagram_username, config.instagram_password)
        url = event.raw_text
        file = "testeee.mp4"

        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Downloading post...')
        instagram.download(url, file)

        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Choosing a comment from post...')
        comment = instagram.choose_comment(url)
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Comment chosen: "{comment}"')

        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Publishing post...')
        instagram.upload(file, comment)
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Post published successfully!')


with client:
    client.run_until_disconnected()
