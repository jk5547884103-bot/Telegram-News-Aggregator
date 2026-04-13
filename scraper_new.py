import asyncio
import os
import feedparser
import sys
from telethon import TelegramClient

# 強制設定輸出編碼，防止中文報錯
sys.stdout.reconfigure(encoding='utf-8')

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
    print(">>> 輿情機器人：啟動系統重試機制...", flush=True)
    
    try:
        api_id = os.environ.get('API_ID')
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id = os.environ.get('TG_CHAT_ID')

        if not all([api_id, api_hash, bot_token, chat_id]):
            print("❌ 錯誤：Secrets 遺失或讀取失敗。", flush=True)
            return

        client = TelegramClient('bot_session_new', int(api_id), api_hash)
        await client.start(bot_token=bot_token)
        
        # 發送報頭
        await client.send_message(int(chat_id), "🗞 **【桑記者的精選輿情 - 系統校準版】**")
        await asyncio.sleep(2)

        for name, url in NEWS_SOURCES.items():
            try:
                print(f">>> 正在抓取: {name}", flush=True)
                feed = feedparser.parse(url)
                
                if feed.entries:
                    msg = f"📍 **{name}**\n"
                    for entry in feed.entries[:4]:
                        title = entry.get('title', '無標題').strip()
                        link = entry.get('link', '#')
                        msg += f"• [{title}]({link})\n"
                    
                    await client.send_message(int(chat_id), msg, link_preview=False)
                    print(f"✅ {name} 發送成功", flush=True)
                    await asyncio.sleep(1)
            except Exception as inner_e:
                print(f"⚠️ {name} 處理時跳過: {inner_e}", flush=True)

        await client.disconnect()
        print(">>> 任務圓滿結束。", flush=True)

    except Exception as e:
        print(f"❌ 嚴重錯誤：{str(e)}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
