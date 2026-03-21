import requests
from bs4 import BeautifulSoup
import time
import csv

original_url="https://www.motac.gov.my/en/kategori-semakan-new/hotel-grading/"
ajax_url = "https://www.motac.gov.my/wp-admin/admin-ajax.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

filename = "motac_hotels.csv"
count = 0

# 使用 'w' 模式初始化文件并写入表头（每次运行脚本会清空旧文件）
with open(filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Index", "Hotel Name", "Address"])

    # 开始循环爬取
    for i in range(0, 5):
        payload = {
            "action": "motac_semakan_filter",
            "kategori": "penggredan-hotel",
            "search": "",
            "negeri": "Wilayah Persekutuan Kuala Lumpur",
            "page": str(i),
            "per_page": "5" 
        }
        
        try:
            print(f"🚀 Retrieving data for page {i}...")
            resp = requests.post(ajax_url, data=payload, headers=headers)
            
            if resp.status_code == 200:
                json_data = resp.json()
                html_content = json_data['data']['html']
                soup = BeautifulSoup(html_content, "html.parser")
                cards = soup.find_all("div", class_="motac-card")

                for card in cards:
                    count += 1
                    name_tag = card.find("div", class_="company-name")
                    address_tag = card.find("div", class_="company-address")
                    
                    name = name_tag.get_text(strip=True) if name_tag else "unknown hotel"
                    address = address_tag.get_text(strip=True) if address_tag else "unknown address"

                    # --- 保存到 CSV ---
                    writer.writerow([count, name, address])
                    
                    print(f"{count}. 🏨 {name} [Saved]")

                time.sleep(2) # 稍微缩短了等待时间
                
            else:
                print(f"❌ Access Failure, error code: {resp.status_code}")

        except Exception as e:
            print(f"⚠️ Error on page {i}: {e}")

print(f"\n✅ All done! Data saved to {filename}")