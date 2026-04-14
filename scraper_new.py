import asyncio
import os
import feedparser
import urllib.request
from telethon import TelegramClient

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

async def fetch_rss_safely(url):
    """偽裝成瀏覽器抓取 RSS，防止被網站擋掉"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return feedparser.parse(response.read())
    except Exception as e:
        print(f">>> 抓取網址時發生網路錯誤: {url}, 原因: {e}")
        return None

async def main():
    print(">>> 系統啟動：進入瀏覽器模擬解析模式...", flush=True)
    
    api_id = os.environ.get('API_ID', '').strip()
    api_hash = os.environ.get('API_HASH', '').strip()
    bot_token = os.environ.get('TG_TOKEN', '').strip()
    chat_id_str = os.environ.get('TG_CHAT_ID', '').strip()

    if not all([api_id, api_hash, bot_token, chat_id_str]):
        print("❌ 錯誤：環境變數不完整。")
        return

    chat_id = int(chat_id_str)
    client = TelegramClient(None, int(api_id), api_hash)
    
    try:
        await client.start(bot_token=bot_token)
        await client.send_message(chat_id, "🗞 **【桑記者的精選輿情 - 瀏覽器模擬版】**")
        
        for name, url in NEWS_SOURCES.items():
            print(f">>> 正在掃描: {name}...", flush=True)
            feed = await fetch_rss_safely(url)
            
            if feed and feed.entries:
                msg = f"📍 **{name}**\n"
                for entry in feed.entries[:4]:
                    title = entry.get('title', '無標題').strip()
                    link = entry.get('link', '#')
                    msg += f"• [{title}]({link})\n"
                
                await client.send_message(chat_id, msg, link_preview=False)
                print(f"✅ {name} 成功發送", flush=True)
                await asyncio.sleep(1.5)
            else:
                print(f"⚠️ {name} 抓取內容為空，可能被該站阻擋。", flush=True)

    except Exception as e:
        print(f"❌ 嚴重錯誤: {e}", flush=True)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
