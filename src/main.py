import os
from datetime import datetime
from telethon import TelegramClient, events

from settings.logger import logger
from settings.config import config

from instagram_bot import InstagramBot



client = TelegramClient('bot', config.telegram_api_id, config.telegram_api_hash).start(
    bot_token=config.telegram_api_bot_token)

async def update_status(message, status):
    return await client.edit_message(message.chat_id, message, f"{message.text}\n{status}")

def is_video(url):
    return "/reel/" in url


@client.on(events.NewMessage(pattern=".*"))
async def my_event_handler(event):
    try:
        if str(config.instagram_url) in event.raw_text:
            logger.info(f"New post received '{event.raw_text}'")
            url = event.raw_text
            file_extension = ".mp4" if is_video(url) else ".jpg"
            file = os.path.join(str(config.downloads_folder), "temp" + file_extension)
            
            message = await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Logging to Instagram...')
            instagram = InstagramBot(
                config.instagram_username, config.instagram_password)

            message = await update_status(message, f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Downloading post...')
            instagram.download(url, file)

            message = await update_status(message, f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Choosing a comment from post...')
            comment = instagram.choose_comment(url)
            message = await update_status(message, f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Comment chosen: "{comment}"')

            message = await update_status(message, f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Publishing post...')
            instagram.upload(file, comment)
            message = await update_status(message, f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> Post published successfully!')
        else:
            logger.info(f"Message received but is not an instagram post '{event.raw_text}'")
            
    except Exception as e: 
        await event.reply(f'🤖 ({datetime.now().strftime("%H:%M:%S")}) -> An error occurred: {e}')

with client:
    client.run_until_disconnected()
