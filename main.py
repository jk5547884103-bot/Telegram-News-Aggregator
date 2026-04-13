import asyncio
import os
import feedparser
import re
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

def clean_html(raw_html):
    """清理 HTML 標籤，確保標題乾淨"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    return cleantext.strip()

async def fetch_and_send(client, chat_id, name, url):
    try:
        print(f">>> 正在處理: {name}", flush=True)
        # 強制重新抓取
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"⚠️ {name} 抓取不到內容", flush=True)
            return

        report_message = f"📍 **{name}**\n"
        count = 0
        
        for entry in feed.entries[:4]:
            # 【關鍵修正】嘗試所有可能的標題與連結欄位
            title = entry.get('title') or entry.get('summary') or entry.get('description') or "新聞標題"
            link = entry.get('link') or entry.get('guid') or entry.get('id') or "#"
            
            # 清理標題中的 HTML 碼
            title = clean_html(title)
            # 如果標題太長（有些 RSS 會把全文塞在標題），截斷它
            if len(title) > 100:
                title = title[:100] + "..."
            
            report_message += f"• [{title}]({link})\n"
            count += 1
        
        if count > 0:
            await client.send_message(chat_id, report_message, link_preview=False)
            print(f"✅ {name} 發送成功", flush=True)
            await asyncio.sleep(1.5) # 稍微加長間隔，增加穩定性
            
    except Exception as e:
        print(f"❌ {name} 錯誤: {e}", flush=True)

async def main():
    print(">>> 輿情機器人啟動：採用【地毯式解析模式】...", flush=True)
    
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
    
    # 發送報頭
    await client.send_message(chat_id, "🗞 **【桑記者的精選輿情早報】**")
    await asyncio.sleep(2)

    # 逐一處理，確保彼此不干擾
    for name, url in NEWS_SOURCES.items():
        await fetch_and_send(client, chat_id, name, url)

    print("✅ 任務執行完畢。", flush=True)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
