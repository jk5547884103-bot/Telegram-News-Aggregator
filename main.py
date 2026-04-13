import asyncio
import os
import feedparser
from telethon import TelegramClient

# 桑記者的精選輿情來源清單 (已移除 TVBS，每家抓取 4 則)
NEWS_SOURCES = {
    "中央社-政治": "https://www.cna.com.tw/rss/aipl.xml",
    "自由時報-政治": "https://news.ltn.com.tw/rss/politics.xml",
    "聯合報-政治": "https://udn.com.tw/rssfeed/news/2/6631?ch=news",
    "中時電子報-政治": "https://www.chinatimes.com.tw/rss/politic.xml",
    "風傳媒-政治": "https://www.storm.mg/feeds/category/118",
    "ETtoday-政治": "https://feeds.feedburner.com/ettoday/politics",
    "鏡週刊-政治": "https://www.mirrormedia.mg/rss/category/political"
}

async def main():
    print(">>> 輿情機器人啟動：正在掃描精選媒體 (每家 4 則)...", flush=True)
    
    # 讀取 GitHub Secrets
    try:
        api_id_env = os.environ.get('API_ID')
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id_env = os.environ.get('TG_CHAT_ID')

        if not all([api_id_env, api_hash, bot_token, chat_id_env]):
            print("❌ 錯誤：GitHub Secrets 設定不完整。", flush=True)
            return

        api_id = int(api_id_env)
        chat_id = int(chat_id_env)
    except Exception as e:
        print(f"❌ 解析環境變數失敗: {e}", flush=True)
        return

    # 建立連線
    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    report_message = "🗞 **【桑記者的精選輿情早報】**\n\n"
    
    for name, url in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                report_message += f"📍 **{name}**\n"
                # 每個媒體抓取最新 4 則
                for entry in feed.entries[:4]:
                    report_message += f"• [{entry.title}]({entry.link})\n"
                report_message += "\n"
        except Exception as e:
            print(f"⚠️ 抓取 {name} 暫時失敗: {e}", flush=True)

    # 發送訊息
    try:
        await client.send_message(chat_id, report_message, link_preview=False)
        print("✅ 報紙送達成功！", flush=True)
    except Exception as e:
        print(f"❌ 發送失敗: {e}", flush=True)
    
    # 強制結束連線
    await client.disconnect()
    print(">>> 程式已安全關閉。", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
