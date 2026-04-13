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
    print(">>> 輿情機器人啟動：採用『逐家發送』模式確保不漏失...", flush=True)
    
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
    
    # 先發送報頭
    await client.send_message(chat_id, "🗞 **【桑記者的精選輿情早報】**")
    await asyncio.sleep(1) # 稍作停頓

    for name, url in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                # 每一家媒體獨立組成一則訊息
                report_message = f"📍 **{name}**\n"
                count = 0
                for entry in feed.entries[:4]:
                    report_message += f"• [{entry.title}]({entry.link})\n"
                    count += 1
                
                if count > 0:
                    await client.send_message(chat_id, report_message, link_preview=False)
                    print(f"✅ {name} 發送成功", flush=True)
                    await asyncio.sleep(0.5) # 防止發送過快
            else:
                print(f"⚠️ {name} 目前沒有新新聞", flush=True)
        except Exception as e:
            print(f"⚠️ 抓取 {name} 失敗: {e}", flush=True)

    print("✅ 所有報紙送達完畢！", flush=True)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
