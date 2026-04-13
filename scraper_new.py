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
    print(">>> 系統啟動，檢查環境變數...", flush=True)
    
    try:
        # 讀取並清理環境變數（防止有空格）
        api_id = os.environ.get('API_ID', '').strip()
        api_hash = os.environ.get('API_HASH', '').strip()
        bot_token = os.environ.get('TG_TOKEN', '').strip()
        chat_id_str = os.environ.get('TG_CHAT_ID', '').strip()

        print(f">>> 目標 Chat ID: {chat_id_str}", flush=True)

        if not all([api_id, api_hash, bot_token, chat_id_str]):
            print("❌ 錯誤：Secrets 設定有缺漏，請檢查 GitHub Settings。", flush=True)
            return

        # 這裡強迫轉換為數字，如果 chat_id 包含 '-' 號也會正確處理
        chat_id = int(chat_id_str)
        
        client = TelegramClient('final_session', int(api_id), api_hash)
        await client.start(bot_token=bot_token)
        
        # 測試發送一則簡單訊息
        await client.send_message(chat_id, "🚀 **輿情系統校準測試：看到這則代表成功了！**")
        await asyncio.sleep(1)

        for name, url in NEWS_SOURCES.items():
            print(f">>> 抓取中: {name}", flush=True)
            feed = feedparser.parse(url)
            if feed.entries:
                msg = f"📍 **{name}**\n"
                for entry in feed.entries[:4]:
                    title = entry.get('title', '無標題')
                    link = entry.get('link', '#')
                    msg += f"• [{title}]({link})\n"
                
                await client.send_message(chat_id, msg, link_preview=False)
                await asyncio.sleep(1)

        await client.disconnect()
        print("✅ 任務全部完成！", flush=True)

    except Exception as e:
        print(f"❌ 執行過程發生錯誤: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
