import requests
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 🔑 API Key và CX ID
API_KEY = "AIzaSyAozat6jJWfrDEGR4Qux_DCCn5UVGlonKY"
CX_ID = "7449493f0a0d34fa2"

# 🔎 Các từ khóa mở rộng
keywords = [
    'pháp luật', 'luật pháp', 'xét xử', 'tòa án', 'công an', 'bản án',
    'vi phạm', 'quy định', 'hình sự', 
]

# 📅 Chia nhỏ thời gian hơn
date_ranges = [
    ('2022-12-31', '2023-02-01'),
    ('2023-01-31', '2023-03-01'),
    ('2023-02-28', '2023-04-01'),
    ('2023-03-31', '2023-05-01'),
    ('2023-04-30', '2023-06-01'),
    ('2023-05-31', '2023-07-01'),
    ('2023-06-30', '2023-08-01'),
    ('2023-07-31', '2023-09-01'),
    ('2023-08-31', '2023-10-01'),
    ('2023-09-30', '2023-11-01'),
    ('2023-10-31', '2023-12-01'),
    ('2023-11-30', '2024-01-01')
]

# 📌 Lưu kết quả
results = []

# 🔄 Chạy nhiều truy vấn
for keyword in keywords:
    for start_date, end_date in date_ranges:
        query = f'site:thanhnien.vn "{keyword}" after:{start_date} before:{end_date}'
        
        for start in range(1, 101, 10):  # Lấy tối đa 100 bài/truy vấn
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX_ID}&start={start}"
            response = requests.get(url)
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    results.append((item["title"], item["link"]))

            if "items" not in data:
                break  # Hết bài báo rồi, dừng lại

# 🏷️ **Hàm kiểm tra ngày đăng của bài báo**
def check_article_date(article):
    title, link = article
    try:
        res = requests.get(link, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        date_tag = soup.find('div', {'data-role': 'publishdate'})
        if date_tag and "2023" in date_tag.text:
            return title, link
    except:
        return None
    return None

# 🔍 **Dùng đa luồng để kiểm tra nhanh hơn**
with ThreadPoolExecutor(max_workers=5) as executor:
    results_2023 = list(executor.map(check_article_date, results))

# 📌 **Lọc bài báo năm 2023**
news_2023 = [r for r in results_2023 if r]

# 📁 **Lưu kết quả vào CSV**
with open("news_phapluat_2023.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["STT", "Tiêu đề", "Link"])
    for index, (title, link) in enumerate(news_2023, start=1):
        writer.writerow([index, title, link])

print(f"\n✅ Đã lưu {len(news_2023)} bài báo vào file news_phapluat_2023.csv!")
