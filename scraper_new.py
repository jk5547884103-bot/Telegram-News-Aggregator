import asyncio
import os
import feedparser
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

async def main():
    api_id = int(os.environ.get('API_ID'))
    api_hash = os.environ.get('API_HASH')
    bot_token = os.environ.get('TG_TOKEN')
    chat_id = int(os.environ.get('TG_CHAT_ID'))

    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    await client.send_message(chat_id, "🗞 **【桑記者的全方位輿情監測 - 系統重啟版】**")
    
    for name, url in NEWS_SOURCES.items():
        try:
            print(f">>> 正在處理: {name}")
            feed = feedparser.parse(url)
            if feed.entries:
                msg = f"📍 **{name}**\n"
                for entry in feed.entries[:4]:
                    msg += f"• [{entry.title}]({entry.link})\n"
                await client.send_message(chat_id, msg, link_preview=False)
                await asyncio.sleep(1) # 間隔防擋
        except Exception as e:
            print(f"❌ {name} 失敗: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
