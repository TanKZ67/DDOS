import requests
from bs4 import BeautifulSoup

# MOTAC 的酒店评级页面
url = "https://www.motac.gov.my/en/kategori-semakan-new/hotel-grading/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"正在访问 MOTAC 官方名录...")

for i in 5:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 寻找表格中的每一行 (tr)
            # 注意：MOTAC 的结构通常是用 <table> 展示数据
            rows = soup.find_all("div",class_="col col-company")

            print("-" * 50)
            i=0
            for row in rows[1:]: # 我们先看前 10 行（跳过表头）
                i+=1
                name_tag = row.find("div", class_="company-name")
                address_tag = row.find("div", class_="company-address")
                
                # 提取文字：如果有这个标签，就拿它的文字并去掉空格；如果没有，就显示“未知”
                name = name_tag.get_text(strip=True) if name_tag else "未知酒店"
                address = address_tag.get_text(strip=True) if address_tag else "未知地址"

                print(i,f"🏨 {name}")
                print(f"📍 {address}")
                print("-" * 50)
        
            print(f"✅ 抓取测试成功！")
        else:
            print(f"访问失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"出错了: {e}")
        
        # 伪代码：寻找“下一页”按钮里的链接
    next_button = soup.find("div", class_="motac-semakan-pagination")
    if next_button:
        # 提取 data-page 属性里的数字 "3"
        next_page_number = next_button.get("data-page")
        print(f"🔗 发现下一页：第 {next_page_number} 页")
        
        # 构造新的网址
        next_url = f"https://www.motac.gov.my/en/.../?page={next_page_number}"
        # 然后让程序去访问这个 next_url
