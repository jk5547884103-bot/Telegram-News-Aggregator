import asyncio
import os
import feedparser
import sys
from telethon import TelegramClient

# 讓輸出立刻顯示在日誌裡
print("--- 程式開始執行 ---", flush=True)

NEWS_SOURCES = {
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml"
}

async def main():
    try:
        # 讀取並檢查變數
        api_id = int(os.environ.get('API_ID', 0))
        api_hash = os.environ.get('API_HASH', '')
        bot_token = os.environ.get('TG_TOKEN', '')
        chat_id = int(os.environ.get('TG_CHAT_ID', 0))

        print(f"嘗試連線 Telegram (ID: {chat_id})...", flush=True)
        
        client = TelegramClient('bot_session', api_id, api_hash)
        await client.start(bot_token=bot_token)
        
        msg = "🗞 **桑記者，輿情機器人測試成功！**\n\n這是一則手動測試訊息。"
        await client.send_message(chat_id, msg)
        
        print("✅ 成功發送訊息到 Telegram！", flush=True)
    except Exception as e:
        print(f"❌ 錯誤發生：{str(e)}", flush=True)
        sys.exit(1) # 強制讓 GitHub 顯示報錯

if __name__ == "__main__":
    asyncio.run(main())
