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

async def fetch_and_send(client, chat_id, name, url):
    """獨立的抓取與發送函數，確保媒體之間互不干擾"""
    try:
        print(f">>> 正在處理: {name}", flush=True)
        # 抓取 RSS
        feed = feedparser.parse(url)
        
        # 如果沒抓到內容
        if not feed.entries:
            print(f"⚠️ {name} 抓取不到內容，可能是網站 RSS 暫時斷線", flush=True)
            return

        report_message = f"📍 **{name}**\n"
        count = 0
        
        # 抓取前 4 則
        for entry in feed.entries[:4]:
            # 優先嘗試不同的標題欄位
            title = entry.get('title') or entry.get('summary') or "無標題"
            link = entry.get('link') or entry.get('guid') or "#"
            
            # 清理標題字串（避免特殊字元造成 Telegram 報錯）
            title = str(title).strip()
            
            report_message += f"• [{title}]({link})\n"
            count += 1
        
        if count > 0:
            await client.send_message(chat_id, report_message, link_preview=False)
            print(f"✅ {name} 發送成功", flush=True)
            await asyncio.sleep(1.2) # 安全間隔
            
    except Exception as e:
        print(f"❌ {name} 發生不可預期錯誤: {e}", flush=True)

async def main():
    print(">>> 輿情機器人啟動：採用【全隔離執行模式】...", flush=True)
    
    try:
        api_id = int(os.environ.get('API_ID'))
        api_hash = os.environ.get('API_HASH')
        bot_token = os.environ.get('TG_TOKEN')
        chat_id = int(os.environ.get('TG_CHAT_ID'))
    except Exception as e:
        print(f"❌ 密鑰讀取錯誤: {e}", flush=True)
        return

    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    # 1. 發送報頭
    await client.send_message(chat_id, "🗞 **【桑記者的精選輿情早報】**")
    await asyncio.sleep(2)

    # 2. 逐一處理媒體（強制隔離）
    for name, url in NEWS_SOURCES.items():
        await fetch_and_send(client, chat_id, name, url)

    print("✅ 所有任務已嘗試執行完畢。", flush=True)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
