import asyncio
import os
import feedparser
import sys
from telethon import TelegramClient

# 測試用：先放一個來源就好，確保能通
NEWS_SOURCES = {"中央社-政治": "https://www.cna.com.tw/rss/aipl.xml"}

async def main():
    print("--- 偵錯模式啟動 ---")
    
    # 讀取 Secrets
    api_id_raw = os.environ.get('API_ID', '')
    api_hash = os.environ.get('API_HASH', '')
    bot_token = os.environ.get('TG_TOKEN', '')
    chat_id_raw = os.environ.get('TG_CHAT_ID', '')

    print(f"檢查 ID 格式: API_ID={api_id_raw[:3]}..., CHAT_ID={chat_id_raw}")

    try:
        api_id = int(api_id_raw)
        chat_id = int(chat_id_raw)
        
        client = TelegramClient('bot_session', api_id, api_hash)
        await client.start(bot_token=bot_token)
        
        msg = "🗞 **桑記者，這是一則自動測試訊息。**\n如果你看到這則訊息，代表連線成功了！"
        await client.send_message(chat_id, msg)
        print("✅ 成功發送測試訊息！請檢查 Telegram。")
        
    except ValueError:
        print("❌ 錯誤：API_ID 或 TG_CHAT_ID 必須是純數字，請檢查 Secrets 是否填錯。")
    except Exception as e:
        print(f"❌ 發生未預期的錯誤: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
