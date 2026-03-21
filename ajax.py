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



# 开始循环爬取
def main():
    Checking=True
    
    while Checking:
        print("Select which function you want")
        print("1. Web Scraper (网页抓取工具)")
        print("2. Convert csv to excel")
        try:
            choice=int(input())            
            if choice ==1:
                webScraper()
                Checking=False
            elif choice==2:
                convertExcel()
                Checking=False
            else:
                Checking=True
                print("out of value")
        except Exception as o:
            print("wrong input: "+str(o))
            
def webScraper():
    count = 0
    
    # 'w' 模式初始化文件并写入表头（每次运行脚本会清空旧文件）
    #"a" 则是append 
    #"r" 则是read
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Hotel Name", "Address"])
    
        for i in range(1, 6):
            payload = {
                "action": "motac_semakan_filter",
                "kategori": "penggredan-hotel",
                "search": "",
                "negeri": "",
                "page": str(i),
                "per_page": "100" 
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

def convertExcel():
    print("excel")


#use __name__ is prevent running failure problem when other script call this script.
#normally run f5, our __name__ whill be __main__ but if i need to call other script by other path python, the __name__ will change to bangumi(file name)

if __name__ == "__main__": 
    main()