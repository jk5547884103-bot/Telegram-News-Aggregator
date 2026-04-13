import asyncio
import os
import feedparser
from telethon import TelegramClient

# 桑記者的精選輿情來源清單
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
    print(">>> 輿情機器人啟動：採用【逐家發送模式】...", flush=True)
    
    try:
        api_id = int(os.environ.get('API_ID'))
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id = int(os.environ.get('TG_CHAT_ID'))
    except Exception as e:
        print(f"❌ Secrets 設定錯誤: {e}", flush=True)
        return

    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    # 先發送總標題
    await client.send_message(chat_id, "🗞 **【桑記者的精選輿情早報】**")
    await asyncio.sleep(1.5)

    for name, url in NEWS_SOURCES.items():
        try:
            print(f">>> 正在抓取: {name}", flush=True)
            feed = feedparser.parse(url)
            
            if not feed.entries:
                print(f"⚠️ {name} 目前無新內容，跳過。", flush=True)
                continue

            report_message = f"📍 **{name}**\n"
            news_count = 0
            
            # 抓取最新 4 則
            for entry in feed.entries[:4]:
                title = entry.get('title', '無標題')
                link = entry.get('link', '#')
                report_message += f"• [{title}]({link})\n"
                news_count += 1
            
            if news_count > 0:
                # 抓到一家就發送一家，確保不漏失
                await client.send_message(chat_id, report_message, link_preview=False)
                print(f"✅ {name} 發送成功", flush=True)
                await asyncio.sleep(1) # 間隔 1 秒防止 Telegram 限制
                
        except Exception as e:
            # 即使這一家失敗，也會繼續抓下一家
            print(f"❌ {name} 抓取或發送失敗: {e}", flush=True)
            continue

    print("✅ 所有媒體處理完畢！", flush=True)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
