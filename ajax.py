import requests
from bs4 import BeautifulSoup
import time

ajax_url = "https://www.motac.gov.my/wp-admin/admin-ajax.php"
headers = {{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest"
},{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}}

count = 0
# range(1, 5) 会跑 1, 2, 3, 4 页
for i in range(1, 5):
    payload = {
        "action": "motac_semakan_filter",
        "kategori": "penggredan-hotel",
        "search": "",
        "negeri": "",
        "page": str(i),
        "per_page": "25" 
    }
    
    try:
        print(f"🚀 正在调取第 {payload['page']} 页数据...")
        resp = requests.post(ajax_url, data=payload, headers=headers)
        
        if resp.status_code == 200:
            # --- 关键修正 1：解析 JSON ---
            json_data = resp.json()
            html_content = json_data['data']['html']
            
            # --- 关键修正 2：用获取到的 HTML 创建 soup ---
            soup = BeautifulSoup(html_content, "html.parser")
            
            # --- 关键修正 3：在 Ajax 结构中，每一项通常叫 motac-card ---
            cards = soup.find_all("div", class_="motac-card")

            print(f"--- 第 {i} 页开始展示 ---")
            
            
            for card in cards:
                count += 1
                name_tag = card.find("div", class_="company-name")
                address_tag = card.find("div", class_="company-address")
                
                name = name_tag.get_text(strip=True) if name_tag else "未知酒店"
                address = address_tag.get_text(strip=True) if address_tag else "未知地址"

                print(f"{count}. 🏨 {name}")
                print(f"   📍 {address}")
                print("-" * 30)

            # 休息一下，模拟真人翻页
            time.sleep(3)
            
        else:
            print(f"❌ 访问失败，错误码: {resp.status_code}")

    except Exception as e:
        print(f"⚠️ 出错: {e}")