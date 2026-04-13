import os

print("--- 測試開始 ---")
token = os.environ.get('TG_TOKEN', '找不到 Token')
chat_id = os.environ.get('TG_CHAT_ID', '找不到 ID')

print(f"Token 長度: {len(token)}")
print(f"Chat ID: {chat_id}")
print("--- 測試結束 ---")
