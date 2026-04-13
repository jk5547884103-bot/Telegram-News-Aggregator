import os
import sys

# 這是強迫日誌輸出的神藥
print("--- 桑記者的程式啟動中 ---", flush=True)

try:
    token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('TG_CHAT_ID')
    print(f"成功讀取變數！Token 長度為: {len(token) if token else '空'}", flush=True)
    print(f"目標聊天 ID: {chat_id}", flush=True)
    
    # 這裡先不做複雜動作，只測試能不能印出這行
    print("✅ 如果你看到這行，代表 main.py 檔案位置正確且成功執行了！", flush=True)
except Exception as e:
    print(f"❌ 發生錯誤: {e}", flush=True)
