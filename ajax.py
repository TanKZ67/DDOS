import requests
from bs4 import BeautifulSoup
import time

ajax_url = "https://www.motac.gov.my/wp-admin/admin-ajax.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

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
        print(f"🚀 Retrieving data for page {payload['page']}...")
        resp = requests.post(ajax_url, data=payload, headers=headers)
        
        if resp.status_code == 200:
            # --- 关键修正 1：解析 JSON ---
            json_data = resp.json()
            html_content = json_data['data']['html']
            
            # --- 关键修正 2：用获取到的 HTML 创建 soup ---
            soup = BeautifulSoup(html_content, "html.parser")
            
            # --- 关键修正 3：在 Ajax 结构中，每一项通常叫 motac-card ---
            cards = soup.find_all("div", class_="motac-card")

            print(f"---  {i} page ---")
            
            
            for card in cards:
                count += 1
                name_tag = card.find("div", class_="company-name")
                address_tag = card.find("div", class_="company-address")
                
                name = name_tag.get_text(strip=True) if name_tag else "unknow hotel"
                address = address_tag.get_text(strip=True) if address_tag else "unknow address"

                print(f"{count}. 🏨 {name}")
                print(f"   📍 {address}")
                print("-" * 30)

            # 休息一下，模拟真人翻页
            time.sleep(3)
            
        else:
            print(f"❌ Acces Failure, error code: {resp.status_code}")

    except Exception as e:
        print(f"⚠️ error: {e}")