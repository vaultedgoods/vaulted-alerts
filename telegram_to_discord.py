from telethon import TelegramClient, events
import requests
import os

# === FILL IN YOUR INFO HERE ===
api_id = 26073909
api_hash = '0b4289a7ba108847174e40805fff5bd7'
discord_webhook_url = 'https://discord.com/api/webhooks/1401730967038591117/p6U-fxWP5xKI35TBfcGn7_pB8Z1E90ZhS-PR-4bQUqwdfk4T4XX_0eONeWe3Ztgzj0W1'
group_username = 'rebeldealz'

# === DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING ===
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=group_username))
async def handler(event):
    message = event.message.message or "(No text)"
    print(f"New Telegram message: {message}")

    if event.message.media:
        file_path = await event.download_media()
        print(f"📸 Image downloaded: {file_path}")

        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'content': message}
            response = requests.post(discord_webhook_url, data=data, files=files)

        os.remove(file_path)
    else:
        data = {"content": message}
        response = requests.post(discord_webhook_url, json=data)

    if response.status_code in [200, 204]:
        print("✅ Sent to Discord!")
    else:
        print(f"❌ Failed to send: {response.status_code}")

print("⏳ Waiting for Telegram messages...")
client.start()
client.run_until_disconnected()
