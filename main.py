import asyncio
import os
import feedparser
from telethon import TelegramClient

NEWS_SOURCES = {
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml",
    "聯合報-政治": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時-政治": "https://www.chinatimes.com.tw/rss/politic.xml"
}

async def main():
    # 讀取你的 Secrets
    api_id = int(os.environ.get('API_ID'))
    api_hash = os.environ.get('API_HASH')
    bot_token = os.environ.get('TG_TOKEN')
    chat_id = int(os.environ.get('TG_CHAT_ID'))

    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    report_message = "🗞 **【桑記者的今日輿情早報】**\n\n"
    for name, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        report_message += f"📍 **{name}**\n"
        # 抓前 3 則新聞
        for entry in feed.entries[:3]:
            report_message += f"• [{entry.title}]({entry.link})\n"
        report_message += "\n"

    await client.send_message(chat_id, report_message, link_preview=False)
    print("✅ 報紙送達成功！")

if __name__ == "__main__":
    asyncio.run(main())
