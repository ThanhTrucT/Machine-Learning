import requests 
from bs4 import BeautifulSoup
import json 

def crawl_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').get_text(strip=True)
    #print(title)

    paragraph = soup.find_all('p')
    content = '\n'.join([p.get_text(strip=True) for p in paragraph])
    #print(content)

    images = []
    for img in soup.find_all('img'):
        img_src = img['src'] if 'src' in img.attrs else ''
        img_caption = img.get('alt', 'No caption')
        images.append({'image': img_src, 'caption': img_caption})
    return{
        'title': title, 
        'content': content, 
        'metadata': images
    }
    
url = 'https://thanhnien.vn/tphcm-chinh-thuc-cong-bo-thong-tin-tuyen-sinh-lop-6-lop-10-185250206085940022.htm'
data = crawl_data(url)

def save_to__json(data, filename='news3.json'):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
       
save_to__json(data)
