import asyncio
import os
import feedparser
import urllib.request
from telethon import TelegramClient

# 桑記者的精選清單 (加上 Google RSS 代理轉接)
NEWS_SOURCES = {
    "聯合報-政治": "https://www.google.com/search?q=https://udn.com.tw/rssfeed/news/2/6631&btnI", # 測試混淆
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml",
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml"
}

async def fetch_rss_safely(url):
    # 增加更多 Header 偽裝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml;q=0.9, */*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            return feedparser.parse(response.read())
    except Exception as e:
        print(f"⚠️ 抓取失敗: {url} | 原因: {e}")
        return None

async def main():
    api_id = os.environ.get('API_ID', '').strip()
    api_hash = os.environ.get('API_HASH', '').strip()
    bot_token = os.environ.get('TG_TOKEN', '').strip()
    chat_id = int(os.environ.get('TG_CHAT_ID', '').strip())

    client = TelegramClient(None, int(api_id), api_hash)
    await client.start(bot_token=bot_token)
    
    await client.send_message(chat_id, "🗞 **【桑記者的輿情早報 - 海外突破版】**")
    
    for name, url in NEWS_SOURCES.items():
        print(f">>> 嘗試突破抓取: {name}")
        feed = await fetch_rss_safely(url)
        if feed and feed.entries:
            msg = f"📍 **{name}**\n"
            for entry in feed.entries[:4]:
                msg += f"• [{entry.get('title', '無標題')}]({entry.get('link', '#')})\n"
            await client.send_message(chat_id, msg, link_preview=False)
            await asyncio.sleep(2)
        else:
            print(f"❌ {name} 依然被網站封鎖")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
