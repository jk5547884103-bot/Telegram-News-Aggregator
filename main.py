
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

# 讀取並檢查環境變數
try:
    API_ID = int(os.environ.get('API_ID', 0))
    API_HASH = os.environ.get('API_HASH', '')
    TG_TOKEN = os.environ.get('TG_TOKEN', '')
    TG_CHAT_ID = int(os.environ.get('TG_CHAT_ID', 0))
except Exception as e:
    print(f"❌ 變數格式錯誤: {e}")

async def main():
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ 錯誤：找不到 TG_TOKEN 或 TG_CHAT_ID，請檢查 GitHub Secrets 設定！")
        return

    try:
        client = TelegramClient('bot_session', API_ID, API_HASH)
        await client.start(bot_token=TG_TOKEN)
        
        report_message = "🗞 **【桑記者的今日輿情早報】**\n\n"
        for name, url in NEWS_SOURCES.items():
            feed = feedparser.parse(url)
            report_message += f"📍 **{name}**\n"
            for entry in feed.entries[:2]:
                report_message += f"• [{entry.title}]({entry.link})\n"
            report_message += "\n"

        await client.send_message(TG_CHAT_ID, report_message, link_preview=False)
        print("✅ 早報發送成功！")
    except Exception as e:
        print(f"❌ 發送失敗，原因：{e}")

if __name__ == "__main__":
    asyncio.run(main())
