import asyncio
import os
import feedparser
import re
from telethon import TelegramClient

# 桑記者的精選輿情 (重新排列順序測試)
NEWS_SOURCES = {
    "聯合報-政治": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml",
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "風傳媒-政治": "https://www.storm.mg/feeds/category/118",
    "ETtoday-政治": "https://feeds.feedburner.com/ettoday/politics",
    "鏡週刊-政治": "https://www.mirrormedia.mg/rss/category/political",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml"
}

async def fetch_and_send(client, chat_id, name, url):
    try:
        print(f">>> 正在嘗試抓取: {name}", flush=True)
        # 加上 agent 偽裝成瀏覽器，防止網站擋掉機器人
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"⚠️ {name} 沒抓到內容，跳過。", flush=True)
            return

        report = f"📍 **{name}**\n"
        for entry in feed.entries[:4]:
            title = entry.get('title', '無標題')
            link = entry.get('link', '#')
            report += f"• [{title}]({link})\n"
        
        await client.send_message(chat_id, report, link_preview=False)
        print(f"✅ {name} 成功發送", flush=True)
        await asyncio.sleep(2) 
    except Exception as e:
        print(f"❌ {name} 失敗: {str(e)}", flush=True)

async def main():
    api_id = int(os.environ.get('API_ID'))
    api_hash = os.environ.get('API_HASH')
    bot_token = os.environ.get('TG_TOKEN')
    chat_id = int(os.environ.get('TG_CHAT_ID'))

    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    await client.send_message(chat_id, "🗞 **【桑記者的全方位輿情監測】**")
    
    for name, url in NEWS_SOURCES.items():
        await fetch_and_send(client, chat_id, name, url)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
