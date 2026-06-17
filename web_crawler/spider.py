import requests
from bs4 import BeautifulSoup
from data_extractor import extract_data
from url_extractor import get_links

seed_url = "https://books.toscrape.com/"
depth = 1



def spider(seed_url , depth):
    queue = []
    docs = []
    queue.append(seed_url)
    for i in range(depth):
            for _ in range(len(queue)): # level order traversal
                current_url = queue.pop(0)
                current_page =  BeautifulSoup(requests.get(current_url).content , "lxml") 
                urls = get_links(current_url, current_page)
                doc = extract_data(current_url,current_page)
                # printing the doc which we got
                print(f"url \n { doc.url }")
                print(f"title\n {doc.title}")
                print(f"body text \n {doc.body_text}")
                print(f"word freq \n {doc.word_freq }")
                docs.append(doc)
                for url in urls:
                    queue.append(url)
                
    return docs



spider(seed_url,1)