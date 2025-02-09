import csv
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor  # Đa luồng

profile_path = r'C:\Users\Tran Thanh Truc\AppData\Local\Google\Chrome\User Data\Profile 1'
options = Options()
options.add_argument(f"user-data-dir={profile_path}")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


service = Service('./chromedriver.exe')
browser = webdriver.Chrome(service=service, options=options)

browser.get("https://thanhnien.vn/giao-duc/tuyen-sinh.htm")
sleep(3)

news_2023 = set()
check = set()
cnt = 0
MAX_ARTICLES = 200 

def fetch_article_date(link):
    try:
        res = requests.get(link, timeout=5)
        soup_article = BeautifulSoup(res.content, 'html.parser')
        data_tag = soup_article.find('div', {'data-role': 'publishdate'})
        if data_tag:
            date = data_tag.text.strip()
            if "2023" in date:
                return link
    except:
        return None
    return None

while cnt < MAX_ARTICLES:

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)

    try:
        show_more = browser.find_element(By.CSS_SELECTOR, ".list__center.view-more.list__viewmore")
        browser.execute_script("arguments[0].click();", show_more)
        print("In process")
    except:
        break

    articles = browser.find_elements(By.CSS_SELECTOR, 'div.box-category-item')
    links = set()

    for article in articles:
        try:
            title_tag = article.find_element(By.TAG_NAME, 'a')
            link = title_tag.get_attribute('href')
            if link and link not in check:
                links.add(link)
                check.add(link)
        except:
            continue

    #Da luong 
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_article_date, links))

    
    for result in results:
        if result and cnt < MAX_ARTICLES:
            news_2023.add(result)
            print(result)
            cnt += 1

browser.quit() 

with open("news_2023.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["STT", "Link Bài Báo"])
    for index, link in enumerate(news_2023, start=1):
        writer.writerow([index, link])

