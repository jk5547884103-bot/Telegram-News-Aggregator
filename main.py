import asyncio
import os
import feedparser
from telethon import TelegramClient

# 新聞來源設定
NEWS_SOURCES = {
    "中央社-政治專欄": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治焦點": "https://news.ltn.com.tw/rss/politics.xml",
    "聯合報-政治要聞": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml"
}

async def main():
    print(">>> 輿情機器人啟動中...", flush=True)
    
    # 讀取 GitHub Secrets
    try:
        api_id = int(os.environ.get('API_ID'))
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id = int(os.environ.get('TG_CHAT_ID'))
    except Exception as e:
        print(f"❌ 讀取 Secrets 失敗: {e}", flush=True)
        return

    # 建立連線
    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    report_message = "🗞 **【桑記者的今日輿情早報】**\n\n"
    
    for name, url in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            report_message += f"📍 **{name}**\n"
            # 每個媒體抓取前 3 則新聞
            for entry in feed.entries[:3]:
                report_message += f"• [{entry.title}]({entry.link})\n"
            report_message += "\n"
        except Exception as e:
            print(f"❌ 抓取 {name} 失敗: {e}", flush=True)

    # 發送訊息
    await client.send_message(chat_id, report_message, link_preview=False)
    print("✅ 報紙發送成功！", flush=True)
    
    # 結束連線（解決跑太久的問題）
    await client.disconnect()
    print(">>> 程式已安全關閉。", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
