import requests
from bs4 import BeautifulSoup
from web_crawler.data_extractor import extract_data
from web_crawler.url_extractor import get_links
from sqlalchemy.orm import Session
import Models

def spider(seed_url , depth , db : Session):
    queue = []
    queue.append(seed_url)
    for i in range(depth):
            for _ in range(len(queue)): # level order traversal
                current_url = queue.pop(0)
                current_page =  BeautifulSoup(requests.get(current_url).content , "lxml") 
                urls = get_links(current_url, current_page)
                doc = extract_data(current_url,current_page)
                new_webpage = Models.webPage(url = doc.url , title = doc.title , body = doc.body_text)
                db.add(new_webpage)
                db.commit()
                db.refresh(new_webpage)
                print(f"url \n { doc.url }")
                print(f"title\n {doc.title}")
                print(f"body text \n {doc.body_text}")
                for url in urls:
                    queue.append(url)

