import requests
import json
from bs4 import BeautifulSoup

def crawl_data(url):
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("h1").get_text(strip=True)
    
    paragraphs = soup.find_all("p")
    content = "\n".join([p.get_text(strip=True) for p in paragraphs])
    

    images = []
    for img in soup.find_all("img"):
        img_src = img["src"] if "src" in img.attrs else ""
        img_caption = img.get("alt", "No caption")
        images.append({"src": img_src, "caption": img_caption})
    
    return {
        "title": title,
        "content": content,
        "images": images
    }
    
def save_to_json(data, filename="news1.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

url = "https://thanhnien.vn/nam-hoc-moi-tuyen-sinh-dau-cap-tai-tphcm-thuc-hien-ra-sao-185250204215811424.htm"
news = crawl_data(url)
save_to_json(news)