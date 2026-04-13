import asyncio
import os
import feedparser
import sys
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# 桑記者的精選清單
NEWS_SOURCES = {
    "聯合報-政治": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml",
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "風傳媒-政治": "https://www.storm.mg/feeds/category/118",
    "ETtoday-政治": "https://feeds.feedburner.com/ettoday/politics",
    "鏡週刊-政治": "https://www.mirrormedia.mg/rss/category/political",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml"
}

async def main():
    print(">>> 系統啟動，進入穩定連線模式...", flush=True)
    
    api_id = os.environ.get('API_ID', '').strip()
    api_hash = os.environ.get('API_HASH', '').strip()
    bot_token = os.environ.get('TG_TOKEN', '').strip()
    chat_id_str = os.environ.get('TG_CHAT_ID', '').strip()

    if not all([api_id, api_hash, bot_token, chat_id_str]):
        print("❌ 錯誤：環境變數設定不完整。", flush=True)
        return

    chat_id = int(chat_id_str)
    
    # 使用 in-memory session 避免檔案衝突
    client = TelegramClient(None, int(api_id), api_hash)
    
    try:
        await client.start(bot_token=bot_token)
        print("✅ Telegram 連線成功！", flush=True)
        
        await client.send_message(chat_id, "🗞 **【桑記者的全方位輿情監測 - 穩定版】**")
        
        for name, url in NEWS_SOURCES.items():
            try:
                feed = feedparser.parse(url)
                if feed.entries:
                    msg = f"📍 **{name}**\n"
                    for entry in feed.entries[:4]:
                        title = entry.get('title', '無標題')
                        link = entry.get('link', '#')
                        msg += f"• [{title}]({link})\n"
                    
                    await client.send_message(chat_id, msg, link_preview=False)
                    print(f"✅ {name} 已送達", flush=True)
                    await asyncio.sleep(2) # 增加發送間隔，防止被禁
            except Exception as e:
                print(f"⚠️ {name} 抓取跳過: {e}", flush=True)

    except FloodWaitError as e:
        print(f"❌ 觸發 Telegram 冷卻機制：請等待 {e.seconds} 秒後再試。", flush=True)
    except Exception as e:
        print(f"❌ 發生錯誤: {e}", flush=True)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
