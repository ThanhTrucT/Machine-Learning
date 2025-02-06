import requests
from bs4 import BeautifulSoup
import json 

def crawl_data(url):
    response = requests.get(url)
    if response.status_code !=200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find('h1').get_text(strip=True)
    
    
    paragraphs = soup.find_all('p') 
    content = '\n'.join([p.get_text(strip = True) for p in paragraphs])
    
    images = []
    for img in soup.find_all('img'):
        img_src = img['src'] if 'src' in img.attrs else ""
        img_caption = img.get('alt', 'No caption')
        images.append({'image': img_src, 'caption': img_caption})
        
    return{
        'title': title,
        'content': content,
        'metadata': images
        
    }
def save_to_json(data, filename='web2.json'):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
url = "https://thanhnien.vn/dang-ky-gian-hang-tu-van-mua-thi-bao-thanh-nien-tang-co-hoi-tiep-can-thi-sinh-185250205142734639.htm"
news = crawl_data(url)
save_to_json(news)

    
    
