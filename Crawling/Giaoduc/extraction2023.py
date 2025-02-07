import requests 
from bs4 import BeautifulSoup
import csv 

url = 'https://thanhnien.vn/giao-duc.htm'

response = requests.get(url)
if response.status_code != 200:
    exit()
    
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all(class_='box-category-item')

news_2023 = []
for article in articles:
    title_tag = article.find('a')
    link = 'http://thanhnien.vn' + title_tag['href']
    
    res = requests.get(link)
    soup_article = BeautifulSoup(res.content, 'html.parser')
    data_tag = soup_article.find('div',{'data-role': 'publishdate'})
    
    if data_tag:
        date = data_tag.text.strip()
        if '2023' in date:
            news_2023.append(link)
    
print(news_2023)
    
    
    
 #   if title_tag and date_tag:
 #       url = 'http://thanhnien.vn' + title_tag['href']
 #       date = date_tag.text.strip
        
 #       if '2023' in date:
 #           news_2023.append([url, date])
       
#with open('news2023.csv', 'w',newline='', encoding='utf8') as f:
   # writer = csv.writer(f)
   # for news in news_2023:
       # writer.writerow(news[url])     

    