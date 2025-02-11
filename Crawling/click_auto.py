import csv
import requests
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Cấu hình Selenium
profile_path = r'C:\Users\Tran Thanh Truc\AppData\Local\Google\Chrome\User Data\Profile 1'
options = Options()
options.add_argument(f"user-data-dir={profile_path}")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Khởi động trình duyệt
service = Service('./chromedriver.exe')
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://thanhnien.vn/thoi-su/phap-luat.htm")
sleep(3)

# Biến toàn cục
news_2023 = []
visited_links = set()
cnt = 0
MAX_ARTICLES = 211
session = requests.Session()

# Thời gian tối đa để cuộn nhanh (giây)
FAST_SCROLL_TIME = 10
start_time = time.time()  

# 🎯 Hàm cuộn nhanh liên tục trong một khoảng thời gian
def fast_scroll():
    while time.time() - start_time <= FAST_SCROLL_TIME:
        browser.execute_script("window.scrollBy(0, 5000);")  
        sleep(2)  # Cuộn nhanh không kiểm tra bài báo

# 🎯 Hàm cuộn chậm
def smooth_scroll():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)  
    try:
        return browser.find_element(By.CSS_SELECTOR, ".list__center.view-more.list__viewmore")
    except:
        return None 

# 🎯 Hàm lấy ngày đăng bài báo
def fetch_article_date(link):
    try:
        res = session.get(link, timeout=3)  
        soup = BeautifulSoup(res.content, 'html.parser')
        date_tag = soup.find('div', {'data-role': 'publishdate'})
        return link if date_tag and "2025" in date_tag.text else None
    except:
        return None

# 🚀 Giai đoạn 1: CUỘN NHANH
print("🚀 Đang cuộn nhanh để tải dữ liệu...")
fast_scroll()
print("✅ Cuộn nhanh hoàn tất! Bắt đầu cuộn chậm...")

# 🚀 Giai đoạn 2: CUỘN CHẬM & CHECK BÀI BÁO 2023
while cnt < MAX_ARTICLES:
    print(f"🔄 Cuộn trang lần {cnt // 10 + 1}...")

    show_more = smooth_scroll()

    if show_more:
        browser.execute_script("arguments[0].click();", show_more)
        print("✅ Nhấn nút 'Xem thêm' thành công!")
        sleep(2)
    else:
        print("⚠ Không tìm thấy nút 'Xem thêm', dừng lại!")
        break

    # 🔍 Lấy danh sách bài báo
    articles = browser.find_elements(By.CSS_SELECTOR, 'div.box-category-item')
    links = []

    for article in articles:
        try:
            title_tag = article.find_element(By.TAG_NAME, 'a')
            link = title_tag.get_attribute('href')
            if link and link not in visited_links:
                links.append(link)
                visited_links.add(link)
        except Exception as e:
            print(f"⚠ Lỗi khi lấy link bài báo: {e}")

    # 🏎️ Dùng đa luồng để kiểm tra ngày bài báo
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_article_date, links))

    # 📌 Lọc bài báo năm 2023
    for result in results:
        if result and cnt < MAX_ARTICLES:
            news_2023.append(result)
            print(f"📌 Bài báo {cnt+1}: {result}")
            cnt += 1

# Đóng trình duyệt sau khi xong
browser.quit()

# 📝 Lưu kết quả vào CSV
with open("news_2023.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["STT", "Link Bài Báo"])
    for index, link in enumerate(news_2023, start=1):
        writer.writerow([index, link])

print("\n✅ Đã lưu kết quả vào file news_2023.csv thành công!")
