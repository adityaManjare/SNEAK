import requests
from bs4 import BeautifulSoup
from sneak.data_extractor import extract_data
from sneak.url_extractor import get_links
from sneak.index_builder import tokenize
from sqlalchemy.orm import Session
from collections import deque
import Models
import json
def spider(seed_url , depth , db : Session):
    metadata = {}
    url_to_docId = {}
    queue = deque()
    is_vis = set()
    is_vis.add(seed_url)
    queue.append(seed_url)
    for i in range(depth):
            for _ in range(len(queue)): 
                current_url = queue.popleft()
                try:
                    response = requests.get(current_url, timeout=4)
                    response.raise_for_status()
                except requests.RequestException:
                    continue

                current_page = BeautifulSoup(response.content, "lxml")
    
                urls = get_links(current_url, current_page)
                doc = extract_data(current_url,current_page)
                new_webpage = Models.webPage(url = doc.url , title = doc.title , body = doc.body_text)
                db.add(new_webpage)
                db.commit()
                db.refresh(new_webpage)
                doc_id = new_webpage.id
                url_to_docId[doc.url] = doc_id
                metadata[doc_id] = {
                    "url": doc.url,
                    "title": doc.title,
                    "length": len(tokenize(doc.title + " " + doc.body_text)),
                    "pagerank": None,
                    "outgoing_links": urls
                }
                for url in urls:
                    if url not in is_vis:
                        queue.append(url)
                        is_vis.add(url)

    N = len(metadata)
    if N == 0 :
         return {}
    initial_rank = 1/N
    for doc_id, info in metadata.items():
        info["pagerank"] = initial_rank
        converted = []
        for url in info["outgoing_links"]:
            if url in url_to_docId:
                converted.append(url_to_docId[url])
        info["outgoing_links"] = converted

    with open("metadata.json" , "w") as f:
         json.dump(metadata,f,indent = 4)
    with open("url_to_docid.json", "w") as f:
        json.dump(url_to_docId, f, indent=4)
    print("completed")
    return metadata


