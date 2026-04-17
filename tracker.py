import requests
from bs4 import BeautifulSoup

# 設定
URL = "https://shop.jollymap.com/zh-HK/product/Hasa-RSX-%E7%AC%AC%E4%BA%8C%E4%BB%A3-Ultegra-Di2-%E5%85%AC%E8%B7%AF%E8%BB%8A%E9%80%A3%E7%A2%B3%E7%BA%96%E7%B6%AD%E8%BC%AA%E7%B5%84/6336?color=12745"
TARGET_PRICE = 20000

# Telegram 設定 (如需通知請填寫)
TELEGRAM_TOKEN = "8671675672:AAGKCFlBRmfBDg2JvPCpDpTTGxiLeRi4UF0" 
TELEGRAM_CHAT_ID = "6274777766"

def send_telegram_msg(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=payload)

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 定位價格 (Jollymap 使用了特定的 meta tag 儲存數值)
        price_tag = soup.find("meta", property="product:price:amount")
        
        if price_tag:
            current_price = float(price_tag['content'])
            print(f"查詢成功！目前價格為: HK${current_price}")
            
            if current_price < TARGET_PRICE:
                msg = f"警報！Hasa RSX 降價了！\n目前價格：HK${current_price}\n連結：{URL}"
                print(msg)
                send_telegram_msg(msg)
            else:
                print("價格尚未達到目標，繼續監控中...")
        else:
            print("錯誤：找不到價格標籤，請檢查網頁是否改版。")
            
    except Exception as e:
        print(f"運行出錯: {e}")

if __name__ == "__main__":
    check_price()
