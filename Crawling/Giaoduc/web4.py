import requests
from bs4 import BeautifulSoup
import json 

def crawl_data(url):
    response = requests.get(url)
    
    if response.status_code !=200:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    wrapper = soup.find(class_='detail-content afcbc-body')
    
    title = soup.find('h1').get_text(strip=True)
    
    for caption in wrapper.find_all(["figcaption", "span"], class_="PhotoCMS_Caption"):
        caption.decompose()
    
    for caption in wrapper.find_all(class_='PhotoCMS_Author'):
        caption.decompose()
        
    paragraph = wrapper.find_all('p')
    content = '\n'.join([p.get_text(strip=True) for p in paragraph])
    
    images = []
    for img in wrapper.find_all('img'):
        img_src = img['src'] if 'src' in img.attrs else ""
        img_caption = img.get('alt', 'No caption')

        images.append([img_src,img_caption])
    
    print(content)
    #print(images)
    
    return{
        'url': url,
        'title': title,
        'content': content,
        'metadata': images
        
    }
    
    
def save(data, filename='news4.json'):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




url = 'https://thanhnien.vn/gian-hang-tai-chuong-trinh-tu-van-mua-thi-niu-chan-hoc-sinh-185240324110052942.htm'
crawl_data(url)

data = crawl_data(url)        
save(data)
