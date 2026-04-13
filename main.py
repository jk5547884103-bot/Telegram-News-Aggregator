import asyncio
import os
import feedparser
import sys
from telethon import TelegramClient

# 強制讓日誌立刻印出來
print(">>> 偵錯訊息：程式已成功啟動", flush=True)

NEWS_SOURCES = {
    "中央社-政治專欄": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治焦點": "https://news.ltn.com.tw/rss/politics.xml",
    "聯合報-政治要聞": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml"
}

async def main():
    try:
        # 讀取環境變數
        api_id_env = os.environ.get('API_ID')
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id_env = os.environ.get('TG_CHAT_ID')

        if not all([api_id_env, api_hash, bot_token, chat_id_env]):
            print("❌ 錯誤：GitHub Secrets 設定不完整，請檢查變數名稱是否正確。", flush=True)
            return

        api_id = int(api_id_env)
        chat_id = int(chat_id_env)

        print(f">>> 偵錯訊息：正在嘗試連線 Telegram (目標 ID: {chat_id})", flush=True)
        
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
        print("✅ 報紙發送成功！", flush=True)
        
    except Exception as e:
        print(f"❌ 發生錯誤：{str(e)}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
